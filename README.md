# key_escrow
A minimal Key Escrow system for LUKS, powered by AWS and Duo

Just two files, unlockLUKS.py is runs on your host to unlock your LUKS volumes, key_escrow.py is a Lambda function to be placed behind API Gateway.

Put a duo.conf and a keys/ directory in an S3 bucket and provide the bucket name in key_escrow.py, and configure your API URL, Duo username and key name in unlockLUKS.py.

When you run unlockLUKS.py from your host, it will query the API, which will send you a Duo push.  If you accept the Duo request, the Duo response will be decorated with a "key" field (the LUKS passphrase) and unlockLUKS.py will unlock and mount your LUKS volumes.
