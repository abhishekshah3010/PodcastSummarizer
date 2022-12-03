# **PODCAST SUMMARIZER**

**TEAM 3**

**OVERVIEW AND GOALS**

A podcast is an audio program or simply a series of spoken word or audio episodes, all focused on a particular topic or theme covering anything from politics and sports to pop culture, journalism, and whatnot. Podcasting is an increasingly popular hobby because of its ease of access which is - it can be listened to whenever and wherever you want. These podcasts or podcast episodes are portrayed to be very long and this can be easily discouraging and distracting for one to hear. Therefore, we developed an idea of summarizing the entire content of the podcast one wishes to hear. But no one will read a paragraph-long summary just to make sure whether they should listen to a podcast or not. So we thought of another way which is, to extract the main points of the podcast, highlight it as a summary and eventually convince one to listen to it all.

We developed and fine-tuned an extractive summarization model that will automatically generate summaries of audio podcasts in approximately 4 to 5 sentences. Extractive summarization is when given a document, we select a subset of the words or sentences that best represents a summary of the document. Additionally, we implemented a sentiment analysis script to detect the sentiment of the summarized text while also designing a web app using Flask for publishing the summarized text along with its sentiment.

**AWS TECHNOLOGIES**

For this project, we will be using the AWS Academy account.

- **S3**

For fulfilling all storage needs.

- **EC2**

For running the frontend application powered by flask.

- **Lambda**

To run our code. We have two lambda functions. One is to convert our audio file to a text file using Transcribe and another one is where our backend model resides.

- **IAM**

For role permissions.

- **Transcribe**

To convert our uploaded audio file to a text file.

- **Comprehend**

To detect the sentiment of the summarized text.

- **Terraform**

IaC to spin up our project.

Along with all these technologies, we are using **flask** for our front end and two prominent python libraries: **sumy** and **nltk**.

**ARCHITECTURE DIAGRAM**

![](RackMultipart20221203-1-pswqon_html_b7eae5380e0bafa9.png)

**Figure 1** : High level architecture

**Terraform (IaC)**

The application uses Terraform as the IaC (Infrastructure as Code) to build all the resources required for the backend to function as well as the EC2 that hosts the frontend Flask application. Terraform requires the user details to run the code. We have provided this to the provider.tf file. Terraform first authenticates the user and then uses these credentials to create all the required resources. Thus, the user also needs access to use all the AWS services.

We utilize the AWS services - S3, Comprehend and Transcribe in the backend and do this by using two Lambda functions and as such, the role specified while creating the Lambda functions required access to these AWS services. Thus, the functions access the Labrole role used by the Academy Accounts that have Full Access to these services.

We also addressed the code format requirements for the Lambda functions. Terraform requires the code to be zipped. We hence provided the code of the two lambda functions and for the two layers required by the summary lambda function as .zip files.

Terraform is thus used to create the following resources:

1. EC2 instance hosting the frontend application.
2. Security groups are required to allow traffic into the front-end web application and the security group network attachment resource.
3. Two Lambda functions along with the required layers and S3 bucket notifications for the triggers.
4. Three S3 buckets.

**Front End Application**

Our front-end application which is deployed on our EC2 instance has various packages installed like:

- **PYTHON3** - Our programming language.
- **PIP3** - Our Python package manager.
- **FLASK** - Our Python web application framework.
- **BOTO3** - This is our Python Software Development Kit (SDK) for AWS which allows us to directly interact with our AWS S3 buckets.
- **GUNICORN3** - Python's HTTP Web Service Gateway Interface (WSGI) server.


The Flask application's user interface provides the functionality to upload an MP3 audio file. A single button is provided to upload and get the summary of the MP3 file. When a valid audio file is selected, the file is uploaded to an authenticated S3 bucket. This authentication is enabled by **AWS Configure** before we run our application. With the AWS configure command we provide our AWS account credentials that allow us to access AWS resources. The uploaded file in the S3 bucket is then picked by the Lambda functions for further backend processing. Once the summary has been extracted in a text file, it is dumped into another S3 bucket and our application renders this text file on the web page.

Our application handles the following edge cases:

1. The uploaded audio file must be of MP3 format only.
2. An audio file can only be less than or equal to 10 mins or 600 seconds.

**Backend -** To perform text summarization and sentiment analysis on the input MP3 file, we first have to convert it into a text file. To do this we use AWS Transcribe and a lambda function - transcribe lambda. The object creation event caused by the front-end application uploading the MP3 into an S3 bucket triggers the lambda function to read the MP3 file and create a Transcribe job. The destination location of the transcribe job is set as a separate S3 bucket. The output of the transcribe job is a json file containing details about the MP3 along with its text content.

 The back-end functionalities including text summarization and sentiment analysis are hosted in a separate Lambda function that runs Python 3.8. The summary lambda utilizes 2 external libraries (nltk and Summy) which were zipped up and imported through the Lamda Layers. We use Luhns's summarizer from the Summy library as our main summarizing algorithm while NLTK was used for tokenizing and stemming the text, as well as importing a list of stopwords from the English language to feed to Luhn's summarizer. Once the json file is detected on the transcribe bucket, the summary lambda will pick up the json file, extract the transcript text, and pass it to the Luhn's summarizer model. Luhn's summarizer will get a list of significant/important words by calculating each word's frequency within the text. Next, each sentence will be scored based on how clustered these words are within the sentence through the Luhn's formula:

where, n = number of significant words

m: its max window span.

![](RackMultipart20221203-1-pswqon_html_c04a211ca4a7cc3e.png)

All sentences will be ranked based on their score in descending order, and the 5 highest scoring sentences will be taken as our extractive summary. After that, we use boto3 to pass this summarized text to AWS Comprehend and receive the sentiment status (of either Mixed, Neutral, Positive, or Negative) back. The summary plus its detected sentiment will be output to a separate S3 bucket. The Flask application will then pick it up from the bucket and display it back to the UI.

**ESTIMATED COSTS**

We calculated the estimated cost for the project under the following assumptions.

- 10,000 users per month
- 2 podcasts per user per day
- 600,000 podcasts per month
- Each podcast is roughly 10 minutes
- Each podcast is roughly 1200-1500 words
- Region as us-east-1

**AWS S3 -** We are using three S3 buckets: For storing uploaded MP3(input bucket), for storing transcribed text(transcribe-output), and for storing summarized text(summary bucket).

For both, the input bucket and transcribe-output buckets, we will be storing the data as well as fetching the data from the input bucket to the transcribe-output bucket and from the transcribe-output bucket to the summary bucket. Therefore, we considered 600,000 requests for PUT, COPY, POST, and LIST and 600,000 requests for GET, and SELECT as we assumed 600,000 podcasts per month for which we require 3.26 USD per month for each bucket. For the summary bucket, we considered 600,000 PUT, COPY, POST, and LIST requests only as we are not dealing with any GET or SELECT operation. This will be costing us 3.02 USD every month. The output from this bucket is directly fetched by the frontend.

**AWS Transcribe -** We use Transcribe to convert our uploaded audio file to a text file. Based on our assumptions, we will be requiring 18,00,000 minutes of processing per month. The estimated cost for this batch processing was 25,410 USD per month.

![](RackMultipart20221203-1-pswqon_html_abe2db92e7f249b8.png)

**Figure 2** : AWS technologies estimated costs

**AWS EC2 -** We will be using 2 EC2 instances: Terraform EC2 and Frontend EC2. Terraform EC2 runs the terraform script, setting up the resources required for the project for which we require t2.large as instance type and a storage amount of 30GB. The estimated cost per month for this was around 44.98 USD every month. This terraform script also launched an EC2 instance where our front end runs. This frontend EC2 requires a t2.nano as instance type for which the estimated cost was around 11 USD per month.

**AWS Lambda -** Lambda functions help to run code. We have two lambda functions: Transcribe Lambda and Backend Lambda. Transcribe Lambda helps convert our audio file to a text file and Backend Lambda is where our backend model resides. For the Transcribe lambda, based on the assumptions we considered 600,000 requests every month while also utilizing 0.5 GB of data storage as the transcription job will require some space for json files. The estimated cost for this was around 68.33 USD. The Backend lambda is comparatively cheap even with 600,000 requests as we are not utilizing any storage space. The cost for this is 0.00 USD.

**AWS Comprehend -** We use Comprehend to detect the sentiment of the summarized text. Considering 600,000 documents every month with 1500 average characters in documents, the estimated cost for every month was around 900 USD.

Overall, it costs 317,326 USD for a year which is around 26500 USD every month considering 10,000 users using the application for about 2 podcasts each day. When it comes to just a single user, the application is very cheap and will just cost around 2.7 USD per day.

![](RackMultipart20221203-1-pswqon_html_35cbdc87a15a8c8a.png) **Figure 3** : Overall and monthly cost

