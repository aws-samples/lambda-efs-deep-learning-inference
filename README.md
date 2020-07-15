# Deep Learning inference with AWS Lambda and Amazon EFS

## Introduction

[Amazon EFS support for AWS Lambda](https://aws.amazon.com/about-aws/whats-new/2020/06/aws-lambda-support-for-amazon-elastic-file-system-now-generally-/?nc1=h_ls) enables storing large deep learning (DL) framework libraries and models on Amazon EFS and load from Lambda.

This repository shows and example of how to use such capability to host a pre-trained Tensorflow 2 object detection model (SSD) from TensorFlow Hub and execute inferences.

Using EFS and Lambda for deep learning inference requires to execute two steps:

1.	Storing the deep learning libraries and model on EFS
2.	Creating a Lambda function for inference, which loads the libraries and model from the EFS file system

The steps above are executed by deploying the project via the [AWS CDK](https://aws.amazon.com/cdk/) and then using [AWS CodeBuild](https://aws.amazon.com/codebuild/) for installing the required libraries to EFS.

## Running the example

To run this example:

```
# Install the AWS CDK and bootstrap the target account (if this was never done before)
$ npm install -g aws-cdk
$ cdk bootstrap aws://{account_id}/{region}

```

```
# clone repository
$ git clone https://github.com/giuseppeporcelli/lambda-efs-ml-demo.git
$ cd lambda-efs-ml-demo
```

```
# Install packages for the project, build and deploy
$ cd cdk/
$ npm install
$ npm run build
$ cdk deploy
```

After deployment, note the output:

```
Outputs:
LambdaEFSMLDemo.LambdaFunctionName = 
LambdaEFSMLDemo-LambdaEFSMLExecuteInference17332C2-0546aa45dfXXXXXX
```

It takes a few minutes for AWS CodeBuild to deploy the libraries and framework to EFS. To test the Lambda function, run this command, replacing the function name:

```
$ aws lambda invoke \
    --function-name LambdaEFSMLDemo-LambdaEFSMLExecuteInference17332C2-0546aa45dfXXXXXX \
    --region us-east-1 \
    --cli-binary-format raw-in-base64-out \
    --payload '{"url": "https://images.pexels.com/photos/310983/pexels-photo-310983.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"}' \
    --region us-east-1 \
    /tmp/return.json    
```

This is the output:

```
{
    "StatusCode": 200,
    "ExecutedVersion": "$LATEST"
}
```
Here you can check the inference’s result:

```
$ tail /tmp/return.json 

{"statusCode": 200, "body": "{\"detection_boxes\": [[0.4908023476600647, 0.29575252532958984,
0.9392691254615784, 0.7548272609710693], [0.2890659272670746, 0.44450390338897705, 
0.8515050411224365, 0.6895579099655151], [0.700944721698761, 0.5776023864746094, 
0.9346526265144348, 0.763191819190979], [0.6840880513191223, 0.3130854070186615, 
0.9327453970909119, 0.4774819314479828], [0.6840880513191223, 0.3130854070186615, 
0.9327453970909119, 0.4774819314479828], [0.700944721698761, 0.5776023864746094, 
0.9346526265144348, 0.763191819190979], [0.2874983847141266, 0.4483768939971924, 
0.8595395088195801, 0.6886227130889893], [0.7860985994338989, 0.06227143853902817, 
0.8351912498474121, 0.1968214511871338], [0.7888965010643005, 0.5248408913612366, 
0.861912190914154, 0.5945348143577576], ...

```

Additionally, you can use the Jupyter notebook in the [notebook](./notebook) folder to print bounding boxes on images.

### Destroy the stack

```
# Afterwards, you can destroy the stack with
$ cdk destroy
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

The contents of this repository are licensed under the [MIT-0 License](./LICENSE).
<br />
Third party content is licensed under the [Apache-2.0 License](./THIRD-PARTY-LICENSES).

## Authors

[Giuseppe A. Porcelli](https://it.linkedin.com/in/giuporcelli) - Principal, ML Specialist Solutions Architect - Amazon Web Services EMEA<br />
[Diego Natali](https://www.linkedin.com/in/diego-natali) - Sr. Solutions Architect - Amazon Web Services EMEA
