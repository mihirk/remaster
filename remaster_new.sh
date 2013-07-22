echo "Enter Ubuntu image filename - "
read path
uck-remaster-unpack-iso $path
uck-remaster-prepare-alternate
echo "Enter the new software required - "
read reqd
echo "Enter the final image installation size - "
read size
python ml.py $size $reqd
FILENAME="download"
cp download ~/tmp/remaster-iso/pool/extras/
cp downloadl ~/
cd ~/tmp/remaster-iso/pool/extras/

cat $FILENAME | while read LINE
do
       apt-get download $LINE
done
FILENAME="downloadl"
cd ~
mkdir pkgdown
cp downloadl pkgdown/
cd pkgdown

cat $FILENAME | while read LINE
do
       apt-get download $LINE
done
tar  -zcvpf ~/pkgdown.tar.gz ~/pkgdown
echo "Enter GPG Key - "
read key
uck-remaster-finalize-alternate $key 
uck-remaster-pack-iso
mv ~/tmp/remaster-iso/livecd.iso .
uck-remaster-clean
