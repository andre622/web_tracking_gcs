## Setup

Before you can run or deploy the sample, you will need to do the following:

1. Enable the Cloud Pub/Sub API in the [Google Developers Console](https://console.developers.google.com/project/_/apiui/apiview/pubsub/overview).

2. Create a topic and subscription.

        $ gcloud alpha pubsub topics create [your-topic-name]
        $ gcloud alpha pubsub subscriptions create [your-subscription-name] \
            --topic [your-topic-name] \
            --push-endpoint \
                https://[your-app-id].appspot.com/pubsub/push?token=[your-token] \
            --ack-deadline 30

3. Update the environment variables in ``app.yaml``.

## Running on App Engine

Deploy using `gcloud`:

    gcloud app deploy app.yaml

You can now access the application at `https://your-app-id.appspot.com`. You can use the form to submit messages, but it's non-deterministic which instance of your application will receive the notification. You can send multiple messages and refresh the page to see the received message.
