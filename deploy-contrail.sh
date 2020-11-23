#!/bin/bash

/snap/bin/juju destroy-model contrail <<-EOF
y
EOF

git pull origin master &&

/snap/bin/juju add-model contrail && 

if [ $2 = "queens" ]; then
	filename=contrail-docker-bundle-queens-bionic.yaml
elif [ $2 = "train" ]; then
	filename=contrail-docker-bundle-train-bionic.yaml
else
	if [ $1 = "focal" ]; then
		filename=contrail-docker-bundle-ussuri-focal.yaml
	else
		filename=contrail-docker-bundle-ussuri-bionic.yaml
	fi
fi

sed -i "s/image-tag.*/image-tag: \"$3\"/g" $filename &&

/snap/bin/juju deploy ./$filename
