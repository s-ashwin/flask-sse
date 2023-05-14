from gevent import monkey

from messenger import Messenger; monkey.patch_all()
from flask import Flask, Response, render_template, request
from gevent.pywsgi import WSGIServer
import json

app = Flask(__name__)

def format_sse(data: str, event=None) -> str:
    _data = json.dumps(data)
    msg = f'data: {_data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg

messenger = Messenger()


@app.route('/newmessage', methods = ['POST'])
def ping():
    print(request.get_json())
    msg = format_sse(data=request.get_json(), event='message')
    messenger.publish(msg=msg)
    return {}, 200

@app.route("/")
def render_index():
  return render_template("index.html")

@app.route("/listen")
def listen():

  def stream():
        messages = messenger.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg

  return Response(stream(), mimetype='text/event-stream')

if __name__ == "__main__":
  app.run(host="0.0.0.0",port=3000, debug=True)
  http_server = WSGIServer(("localhost", 3000), app)
  http_server.serve_forever()








