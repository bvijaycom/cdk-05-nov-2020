from aws_cdk import (
    aws_s3 as s3,
    aws_s3_deployment as s3upload,
    core,
    aws_events as events,
    aws_lambda as lambda_,
    aws_events_targets as targets,
    aws_dynamodb,
    aws_iam,
)



class SecondStack(core.Stack):
    def __init__(self, app: core.App, id: str) -> None:
        super().__init__(app, id)

        _lambda_name = core.CfnParameter(self, "LambdaName", type="String")
        _lambda_Role_name = _lambda_name.value_as_string + 'Role'
        _lambda_Rule_name = _lambda_name.value_as_string + 'Rule'


        iamRole = aws_iam.Role(self,
                               "lambdaUniqueID",
                               role_name=_lambda_Role_name,
                               assumed_by=aws_iam.ServicePrincipal(
                                   "lambda.amazonaws.com")
                               )

        iamRole.add_to_policy(aws_iam.PolicyStatement(
            effect=aws_iam.Effect.ALLOW,
            actions=["logs:CreateLogGroup",
                     "logs:CreateLogStream",
                     "logs:PutLogEvents",
                     "cloudwatch:*",
                     "dynamodb:*",
                     "s3:*"],
            resources=["*"]
        ))

        with open("../files/lambda-handler2.py", encoding="utf8") as fp:
            handler_code = fp.read()

        lambdaFunction = lambda_.Function(
            self, "Singleton",
            function_name=_lambda_name.value_as_string,
            code=lambda_.InlineCode(handler_code),
            handler="index.main",
            timeout=core.Duration.seconds(300),
            runtime=lambda_.Runtime.PYTHON_3_7,
            role=iamRole
        )

        # Run Every 5 minutes between 8:00 AM and 5:55 PM weekdays
        # See https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html
        rule = events.Rule(
            self, "Rule",
            rule_name=_lambda_Rule_name,
            schedule=events.Schedule.cron(
                minute='0/5',
                hour='*',
                month='*',
                week_day='MON-FRI',
                year='*'),
        )

        rule.add_target(targets.LambdaFunction(lambdaFunction))


app = core.App()
SecondStack(app, "taskTwoStack")
app.synth()
