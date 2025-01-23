from flask import Blueprint, jsonify, request, redirect
from models.url import Url
from utils.db import db
from models.urlSchema import UrlSchema, url_schema, urls_schema

main=Blueprint('url_blueprint', __name__)

@main.route('/urls')
def get_urls():
    try:
        urls = Url.query.all()
        result = urls_schema.dump(urls)
        return jsonify(result)
    except Exception as ex:
        return jsonify({'message': str(ex)}),500

@main.route('/', methods=['POST'])
def get_url():
    url = request.args.get('url')
    try:
        try:
            short_url = Url.query.filter_by(original_url = url).one()
        except Exception as NotFound:
            new_url = Url(url)
            db.session.add(new_url)
            db.session.commit()
            new_url.set_short_url()
            db.session.commit()
            short_url = Url.query.filter_by(original_url = url).one()
        result = url_schema.dump(short_url)        
        return jsonify(result)
    except Exception as ex:
        return jsonify({'message': str(ex)}),500
    
@main.route('/<id>')
def redirectUrl(id):
    try:
        url = Url.query.get(id)
        if url is not None:
            result = url_schema.dump(url) 
            return redirect(result['original_url'])
        else: return jsonify({'message': "Short Url Does Not Exist"}),404
    except Exception as ex:
        return jsonify({'message': str(ex)}),500  