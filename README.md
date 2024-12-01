# Hands-on: Message Brokers

This project contains two folders, `event-driven` and `pipes-and-filters` each for their respective approach.
Despite the differences in approaches, the building and usage process is almost identical.

## 🔨 Build process

> Before starting either of approaches, make sure to create `.env` file in either/both of the folders that contains `EMAIL_ADDRESS` and `EMAIL_PASSWORD` as shown in `.env.example`, this data will be used to send the emails from.

To startup, just do the `docker compose up` in either of the directories.

## ✨ Usage

After building, you will have access to new endpoint: `localhost:5000/send`, to which you can send a `POST` request that contains `json` with two fields: `user_alias` (it will say who sent the message) and `message` (the text itself).

> you can use following curl command to do just that: <br/>
> `curl -X POST --data '{"message": "message text", "user_alias": "Professor"}' --header 'Content-Type: application/json'  localhost:5000/send`

##  ✅ Monitoring

### The Event Driven Approach

The **RabbitMQ** as a message broker provides incredibly robust dashboard for tracking all messages and how much resources they use that can be accessed at `http://127.0.0.1:15672/` and rather insightful logs in docker.

### The Pipes And Filters Approach

Unlike **RabbitMQ**, it can't show off as much information, but you can still track which specific service was more likely responsible for the failure by getting back information on how far into the system your message went with json response that will look something like this:

```json
{
  "filter_response": {
    "screaming_response": {
      "publish_response": {
        "status": "Email sent"
      },
      "status": "Message forwarded"
    },
    "status": "Message forwarded"
  },
  "status": "Message forwarded"
}
```
