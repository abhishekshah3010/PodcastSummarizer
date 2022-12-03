For the application to run, I'll have to share the following AMIs with your AWS account. 

1. PodcastSummarizer_Terraform - This AMI contains the terraform script. Create an EC2 using this AMI.
2. PodcastSummarizer_Frontend - This AMI contains the frontend application. The terraform script will create an EC2 instance using this AMI.


Podcasts Submitted - 
The Sample_Podcasts.zip file contains 5 sample podcasts. You can use these to test the application.Unzip the files and save to local.


Time Required - 
1. To run the Terraform script and create all resources (18 resources created) - 5 mins
2. To get the summary once the MP3 is uploaded - 3 mins
3. To destroy all the resources created by Terraform - 3 min


Steps to Create the Resources required by the System -
1. Instantiate an EC2 instance using the AMI containing Terraform code.
   a. Select Key Pair
   b. Size of EC2 instance t2.large
   c. Configure Storage to be 30 GB instead of 8 GB
2. Login to CloudShell and connect to EC2. Ensure you connect as ec2-user.
3. Add your account credentials (access_key, secret_key, token) to the file - provider.tf in the provider block. Run the following command-
		$ nano provider.tf
4. Add your key name in the file -  terraform.tfvars on line 2. Run the following command -
		$ nano terraform.tfvars
5. Run the following commands-
		$ terraform init
		$ terraform apply
	Type ‘yes’ and press enter
6. This will create all the required resoucres. Number of resources created should be 18.


Steps to Start the Web Application -
1. Login to CloudShell and connect to EC2 created by Terraform - Summarizer_FrontEnd. Ensure you connect as ec2-user.
2. You will have to edit the .aws/credentials file to include the token. Run the following command to add the token as value to the variable - aws_session_token
		$ nano .aws/credentials
3. To start the frontend application run the command  - 
		$ python3 send_data_to_aws.py
4. Open the frontend application by using the Public IPv4 address of the Summarizer_FrontEnd EC2 and appending - :8080 to it. Example - 18.206.94.160:8080


Steps to use the Web Application -
1. Click on the Choose File button and select the MP3 you want to get the summary for.
2. Click on Upload.
3. Wait while the application retrieves the summary and it is displayed.
4. You can do this for multiple files.
5. Keep the web application page open while a summary is extracted. This can take a couple of minutes.


Steps to Stop the Application and Destroy all Resouces -
1. Go to CloudShell of the Summarizer_FrontEnd instance.
2. Press Control + C.
3. Go to CloudShell of Terraform instance.
4. Run the command 
		$ terraform destroy
5. Type yes and click enter.
6. Make sure you delete the Terraform EC2 instance.