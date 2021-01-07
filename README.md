# Pre-requisites
Deploy (bootstrap) juju-controller with ubuntu focal

# Python juju-auto-deployment
Required files:
1. juju-python-deployment.py
2. deploy-contrail.sh
3. Modify bundle yaml file(s): contrail-docker-bundle-ussuri-focal.yaml or contrail-docker-bundle-ussuri-bionic.yaml or contrail-docker-bundle-queens-bionic.yaml or contrail-docker-bundle-train-bionic.yaml


#Command line execution:
-----------------------
> Deploy from inside tf-charms

```sh
$ python juju-python-deployment.py -u bionic -o ussuri -c 2011.98
```


 Output:
 -------
 result.txt
 #Comment on/off write_result() in main() of juju-python-deployment.py
