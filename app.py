from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.jszei2q.mongodb.net/?retryWrites=true&w=majority')
db = client.dbProject

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/tracker", methods=["POST"])
def tracker_post():
    problem_receive = request.form['problem_give']
    link_receive=request.form['link_give']
    difficulty_receive=request.form['difficulty_give']
    count= db.tracker.count_documents({})
    num=count+1
    doc={
        'num':num,
        'problem':problem_receive,
        'link':link_receive,
        'difficulty':difficulty_receive,
        'status':0
    }
    db.tracker.insert_one(doc)
    # bucket_receive = request.form['bucket_give']
    # count = db.bucket_db.count_documents({})
    # num=count+1
    # # print(sample_receive)
    # doc={
    #     'num':num,
    #     'bucket':bucket_receive,
    #     'done':0
    # }
    # db.bucket_db.insert_one(doc)
    return jsonify({'msg': 'Data Saved Successfully!'})

@app.route("/tracker/delete", methods=["POST"])
def tracker_delete():
    num_receive = request.form['num_give']
    db.tracker.delete_one({'num': int(num_receive)})
    return jsonify({'msg': 'Delete Done!'})

@app.route("/tracker/status/solved", methods=["POST"])
def tracker_done_solved():
    num_receive = request.form['num_give']
    db.tracker.update_one({'num':int(num_receive)},{'$set':{'status':1}})
    # num_receive = request.form['num_give']
    # # print(sample_receive)
    # db.bucket_db.update_one({'num':int(num_receive)},{'$set':{'done':1}})
    return jsonify({'msg': 'Status Updated !'})

@app.route("/tracker/status/unsolved", methods=["POST"])
def tracker_done_unsolved():
    num_receive = request.form['num_give']
    db.tracker.update_one({'num':int(num_receive)},{'$set':{'status':0}})
    # num_receive = request.form['num_give']
    # # print(sample_receive)
    # db.bucket_db.update_one({'num':int(num_receive)},{'$set':{'done':1}})
    return jsonify({'msg': 'Status Updated !'})
@app.route("/tracker/count", methods=["GET"])
# def tracker_get():
#     tracker_list=list(db.tracker.find({},{'_id':False}))
#     return jsonify({'list':tracker_list,'msg': 'Get request Done!'})
#     # buckets_list = list(db.bucket_db.find({},{'_id':False}))
#     # return jsonify({'buckets':buckets_list})
#     return jsonify({'msg': 'Get request Done!'})

@app.route("/tracker", methods=["GET"])
def tracker_get():
    tracker_list=list(db.tracker.find({},{'_id':False}))
    count_total=db.tracker.count_documents({})
    count_solved=db.tracker.count_documents({'status':1})
    count_unsolved=db.tracker.count_documents({'status':0})
    return jsonify({'list':tracker_list,'msg': 'Get request Done!','ctotal':count_total,'stotal':count_solved,'utotal':count_unsolved})
    # buckets_list = list(db.bucket_db.find({},{'_id':False}))
    # return jsonify({'buckets':buckets_list})
    return jsonify({'msg': 'Get request Done!'})
if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)