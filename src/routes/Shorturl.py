from flask import Blueprint, jsonify, request, redirect
# Models
from models.ShorturlModel import ShorturlModel

main=Blueprint('shorturl_blueprint', __name__)

@main.route('/urls')
def get_urls():
    try:
        urls=ShorturlModel.get_urls()
        return jsonify(urls)
    except Exception as ex:
        return jsonify({'message': str(ex)}),500
    
@main.route('/', methods=['POST'])
def get_url():
    url = request.args.get('url')
    try:
        short_url = ShorturlModel.get_shorturl(url)
        if short_url != None:
            return jsonify(short_url)
        else:
            ShorturlModel.create_shorturl(url)
            short_url = ShorturlModel.get_shorturl(url)
            return jsonify(short_url),201

    except Exception as ex:
        return jsonify({'message': str(ex)}),500
    

@main.route('/<index>')
def redirectUrl(index):
    try:
        url = ShorturlModel.get_originalUrl(index)
        if url is not None:
            return redirect(url)
        else: return jsonify({'message': "Short Url Does Not Exist"}),404
    except Exception as ex:
        return jsonify({'message': str(ex)}),500   