# Python juju-auto-deployment
Required files:
1. juju-python-deployment.go
2. deploy-contrail.sh
3. Atleast one bundle yaml file: contrail-docker-bundle-queens.yaml or contrail-docker-bundle-ussuri.yaml or contrail-docker-bundle-train.yaml 


Command line execution:
-----------------------
> Deploy from inside tf-charms

```sh
$ python juju-python-deployment.py queens 2008.12
```

 
 Output:
 -------
 result.txt
 #Comment on/off write_result() in main() of juju-python-deployment.py
