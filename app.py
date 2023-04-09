from flask import Flask, render_template, Response
from formChecker import gen_frames
app = Flask(__name__)

#defines route for homepage to render html file
@app.route('/')
def index():
    return render_template('index.html')

#helper function called by video_feed(). Opens webcam and records user.
#video_feed() function is ran when requests /video_feed url
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__': #checks if current file is ran as main script
    app.run(port=8000, debug=True) #starts flask dev server 