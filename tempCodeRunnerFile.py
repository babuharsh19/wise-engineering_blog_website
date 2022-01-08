@app.route("/post/<post_slug>", methods=['GET'] )
# @login_required
# def post_fetch(post_slug):
#     post = Post.query.filter_by(slug=post_slug).first()
#     return render_template('post.html',param=parameter,post=post)