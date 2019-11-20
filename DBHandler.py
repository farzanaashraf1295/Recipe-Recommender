from datetime import datetime

from utils.DBUtils import DBUtils


class DBHandler:

    @staticmethod
    def register(user):
        db = DBUtils.get_instance()

        username = user['username']
        sql = "SELECT * FROM login WHERE username = '{}'".format(username)
        result = db.get(sql)
        if result:
            return -1

        sql = "INSERT INTO login (username, password, userType, active) VALUES (%s, %s, %s, %s)"
        login_id = db.insert(sql=sql, args=(username, user['password'], 'user', 0))
        print(login_id)

        sql = "INSERT INTO user (loginId, fullname, email) VALUES (%s, %s, %s)"
        db.insert(sql=sql, args=(int(login_id), user['fullname'], user['email']))

        return login_id

    @staticmethod
    def login(user):
        db = DBUtils.get_instance()

        sql = "SELECT * FROM login WHERE username = '{}' AND password = '{}'".format(user['username'], user['password'])
        result = db.get(sql)
        return result

    @staticmethod
    def save_recipe(recipe):
        db = DBUtils.get_instance()

        sql = "INSERT INTO recipe (name, category, description, image, featured) VALUES (%s, %s, %s, %s, %s)"
        recipeId = db.insert(sql,
                             (recipe['name'], recipe['category'], recipe['description'], recipe['image'],
                              recipe['featured']))

        ingredients = recipe['ingredients']
        for ingredient in ingredients:
            sql = "INSERT INTO recipeingredient (recipeId, ingredient) VALUES (%s, %s)"
            db.insert(sql, (recipeId, ingredient['ingredient']))

        directions = recipe['directions']
        order = 1
        for direction in directions:
            sql = "INSERT INTO recipedirection (recipeId, `order`, direction) VALUES (%s, %s, %s)"
            db.insert(sql, (recipeId, order, direction['direction']))
            order += 1

        return recipeId

    @staticmethod
    def update_recipe(recipe):
        db = DBUtils.get_instance()

        recipeId = recipe['recipeId']

        sql = "UPDATE recipe SET name = '%s', category = '%s', description = '%s', image = '%s', featured = '%s'" \
              "WHERE recipeId = %s"

        db.update(sql, (recipe['name'], recipe['category'], recipe['description'], recipe['image'],
                        recipe['featured'], recipeId))

        sql = "DELETE FROM recipeingredient WHERE recipeId = %s".format(recipeId)
        db.delete(sql)
        sql = "DELETE FROM recipedirection WHERE recipeId = %s".format(recipeId)
        db.delete(sql)

        ingredients = recipe['ingredients']
        for ingredient in ingredients:
            sql = "INSERT INTO recipeingredient (recipeId, ingredient) VALUES (%s, %s)"
            db.insert(sql, (recipeId, ingredient['ingredient']))

        directions = recipe['directions']
        order = 1
        for direction in directions:
            sql = "INSERT INTO recipedirection (recipeId, `order`, direction) VALUES (%s, %s, %s)"
            db.insert(sql, (recipeId, order, direction['direction']))
            order += 1

        return recipeId

    @staticmethod
    def delete_recipe(recipeId):
        db = DBUtils.get_instance()

        sql = "DELETE FROM recipe WHERE recipeId = {}".format(recipeId)
        db.delete(sql)

        sql = "DELETE FROM recipeingredient WHERE recipeId = '{}'".format(recipeId)
        db.delete(sql)

        sql = "DELETE FROM recipedirection WHERE recipeId = '{}'".format(recipeId)
        db.delete(sql)

    @staticmethod
    def get_recipe(category):
        db = DBUtils.get_instance()

        sql = "SELECT * FROM recipe WHERE category = '{}'".format(category)
        result = db.get(sql)

        DBHandler.build_recipe(db, result)

        return result

    @staticmethod
    def build_recipe(db, result):
        if result:
            for res in result:
                sql = "SELECT * FROM recipeingredient WHERE recipeId = '{}'".format(res['recipeId'])
                ingr = db.get(sql)
                res['ingredients'] = ingr

                sql = "SELECT * FROM recipedirection WHERE recipeId = '{}'".format(res['recipeId'])
                dirtn = db.get(sql)
                res['directions'] = dirtn

    @staticmethod
    def add_comment(comment):
        db = DBUtils.get_instance()

        sql = "INSERT INTO recipecomments (recipeId, loginId, comment, commentDate) VALUES (%s, %s, %s, %s)"
        commentId = db.insert(sql, (comment['recipeId'], comment['loginId'], comment['comment'], datetime.now()))

        return commentId

    @staticmethod
    def get_comment(recipeId):
        db = DBUtils.get_instance()
        sql = "SELECT C.commentId, C.comment, C.commentDate, U.fullname " \
              "FROM recipecomments C JOIN user U ON C.loginId = U.loginId WHERE C.recipeId = {}".format(recipeId)
        comments = db.get(sql)
        comments = list(map(lambda x: DBHandler.commentDateParser(x), comments))
        return comments

    @staticmethod
    def commentDateParser(comment):
        commentDate = comment['commentDate']
        comment['commentDate'] = commentDate.timestamp()
        return comment

    @staticmethod
    def save_feedback(feedback):
        db = DBUtils.get_instance()

        sql = "INSERT INTO feedback (loginId, title, feedback, feedbackDate) VALUES (%s, %s, %s, %s)"
        feedbackId = db.insert(sql, (feedback['loginId'], feedback['title'], feedback['feedback'], datetime.now()))

        return feedbackId

    @staticmethod
    def get_feedback():
        db = DBUtils.get_instance()
        sql = "SELECT F.*, U.fullname AS userName FROM feedback F JOIN user U ON F.loginId = U.loginId"
        comments = db.get(sql)
        comments = list(map(lambda x: DBHandler.feedbackDateParser(x), comments))
        return comments

    @staticmethod
    def feedbackDateParser(feedback):
        feedbackDate = feedback['feedbackDate']
        feedback['feedbackDate'] = feedbackDate.timestamp()
        return feedback

    @staticmethod
    def search_recipe(ingredients):
        db = DBUtils.get_instance()

        recipeList = []
        for ingredient in ingredients:
            sql = "SELECT recipeId FROM recipeingredient WHERE ingredient = '{}'".format(ingredient)
            recipeIds = db.get(sql)
            if recipeIds:
                recipeList.append(str(recipeIds[0]['recipeId']))

        recipeList = ','.join(recipeList)
        sql = "SELECT * FROM recipe WHERE recipeId IN ({})".format(recipeList)
        result = db.get(sql)

        DBHandler.build_recipe(db, result)

        return result
