import os
import logging
import subprocess
import timeit
import shlex
import random
import string
import click
from settings import MIXCR_BIN, VDJTOOLS_BIN

class MiXCR:
    def __init__(self, *args, **kwargs):
        chains = ('IGH', 'IGL', 'IGK',
                  'TRA', 'TRB', 'TRG', 'TRD',
                  'IG', 'TCR', 'ALL')
        self.file1 = kwargs.get('file1', None)
        self.file2 = kwargs.get('file2', None)
        self.output_directory = kwargs.get('output_directory', None)
        self.molecule = kwargs.get('molecule', None)
        assert self.file1 is not None
        assert self.file2 is not None
        assert self.output_directory is not None
        assert self.molecule is not None
        assert self.molecule in chains
        self.file1 = os.path.abspath(self.file1)
        self.file2 = os.path.abspath(self.file2)
        self.id = kwargs.get('id',
                             ''.join(random.choices(
                                 string.ascii_uppercase + string.digits, k=10)))

        self.log_file = kwargs.get('log_file', 'mixcr.log')
        self.align_chains = kwargs.get('align_chains', 'ALL')
        self.align_result_file = kwargs.get('align_result_file',
                                            'alignment_result.vdjca')
        self.align_log_file = kwargs.get('align_log_file', 'alignment.log')
        self.align_json_file = kwargs.get('align_log_file', 'alignment.json')
        self.assemble_result_file = kwargs.get('assemble_result_file',
                                               'assemble_result.clone')
        self.assemble_log_file = kwargs.get('assemble_log_file', 'assemble.log')
        self.assemble_json_file = kwargs.get('assemble_log_file', 'assemble.json')
        self.mixcr_export_file_suffix = kwargs.get('mixcr_export_file_suffix',
                                                   '_export.tab')
        self.vdjtools_output_prefix = kwargs.get(
            'vdjtools_output_prefix', 'vdjtools_output')
        self.vdjtools_export_file_suffix = kwargs.get(
            'vdjtools_export_file_suffix', '_clonotype.tab')
        self.mixcr_export_file = self.molecule \
            + self.mixcr_export_file_suffix
        self.vdjtools_export_file = self.molecule \
            + self.vdjtools_export_file_suffix
        assert self.align_chains in chains
        self.overwrite = kwargs.get('overwrite', False)
        self.verbose = kwargs.get('verbose', True)

    def run(self):
        self.before()
        if not(os.path.isfile(self.align_result_file) or
               os.path.isfile(self.assemble_result_file) or
               os.path.isfile(self.mixcr_export_file) or
               os.path.isfile(self.vdjtools_export_file)):
            self.align()
        self.assemble()
        self.export()
        self.convert_to_vdjtools_format()
        self.after()

    def before(self):
        if not os.path.isdir(self.output_directory):
            os.makedirs(self.output_directory)
        self.work_directory = os.getcwd()
        os.chdir(self.output_directory)
        logging.basicConfig(filename=self.log_file, level=logging.DEBUG)
        logging.info('-' * 60)
        logging.info('before()')
        logging.info('Change to directory ' + os.getcwd())

    def after(self):
        logging.info('after()')
        if os.path.isfile(self.align_result_file):
            os.remove(self.align_result_file)
        if os.path.isfile('metadata.txt'):
            os.remove('metadata.txt')
        os.chdir(self.work_directory)
        logging.info('Change to directory ' + os.getcwd())
        logging.info('-' * 60)
        if self.verbose:
            print("Finish!")

    def align(self):
        if os.path.isfile(self.align_result_file) and not self.overwrite:
            logging.info('align(). Skip: result file exists')
            return True
        else:
            logging.info('align()')
        self.align_cmd = MIXCR_BIN + ' align -f -r ' + self.align_log_file \
            + ' -c ' + self.align_chains + ' ' \
            + ' --json-report ' + self.align_json_file + ' ' \
            + ' '.join((self.file1, self.file2, self.align_result_file))
        if self.verbose:
            print("Aligning ...")
        self.align_status = run_subprocess(self.align_cmd)
        return True

    def assemble(self):
        if os.path.isfile(self.assemble_result_file) and not self.overwrite:
            logging.info('assemble(). Skip: result file exists')
            return True
        else:
            logging.info('assemble()')
        self.assemble_cmd = MIXCR_BIN + ' assemble -f -r ' + self.assemble_log_file \
            + ' --json-report ' + self.assemble_json_file + ' ' \
            + ' '.join((self.align_result_file,
                        self.assemble_result_file))
        if self.verbose:
            print("Assmebling ...")
        self.assemble_status = run_subprocess(self.assemble_cmd)
        return True

    def export(self):
        if os.path.isfile(self.mixcr_export_file) and not self.overwrite:
            logging.info('export(). Skip: result file exists')
            return True
        else:
            logging.info('export()')
        self.export_cmd = MIXCR_BIN + ' exportClones -f -c ' \
            + ' '.join((self.molecule,
                        self.assemble_result_file,
                        self.mixcr_export_file))
        if self.verbose:
            print("Exporting ...")
        self.export_status = run_subprocess(self.export_cmd)
        return True

    def convert_to_vdjtools_format(self):
        if os.path.isfile(self.vdjtools_export_file) and not self.overwrite:
            logging.info('convert_to_vdjtools_format(). Skip: result file exists')
            return True
        else:
            logging.info('convert_to_vdjtools_format()')
        self.vdjtools_format_cmd = VDJTOOLS_BIN + ' Convert -S mixcr ' \
            + ' '.join((self.mixcr_export_file,
                        self.vdjtools_output_prefix))
        if self.verbose:
            print("Converting format ...")
        self.format_status = run_subprocess(self.vdjtools_format_cmd)
        filename, file_ext = os.path.splitext(self.mixcr_export_file)
        infile = self.vdjtools_output_prefix + '.' + filename + '.txt'
        os.rename(infile, self.vdjtools_export_file)
        return True


def run_subprocess(cmd):
    logging.info('Subprocess: ' + cmd)
    start_time = timeit.default_timer()
    try:
        command_line_process = subprocess.Popen(
            shlex.split(cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        process_output, _ = command_line_process.communicate()
        logging.info(process_output)
    except (OSError, subprocess.CalledProcessError) as exception:
        logging.info('Exception occured: ' + str(exception))
        logging.info('Subprocess failed')
        return False
    else:
        stop_time = timeit.default_timer()
        logging.info('Subprocess finished. ' +
                     str(stop_time - start_time) + ' seconds.')
        return True
