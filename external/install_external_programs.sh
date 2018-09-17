# Create directory
mkdir -p external
cd external
# MiXCR
curl -OL https://github.com/milaboratory/mixcr/releases/download/v2.1.12/mixcr-2.1.12.zip
unzip -a mixcr-2.1.12.zip
rm -f mixcr-2.1.12.zip
mv mixcr-2.1.12 mixcr
# VDJtools
curl -OL https://github.com/mikessh/vdjtools/releases/download/1.1.10/vdjtools-1.1.10.zip
unzip -a vdjtools-1.1.10.zip
rm -f vdjtools-1.1.10.zip
mv vdjtools-1.1.10 vdjtools
cd ../
