from ..extensions import db, ma, Resource, Api, Blueprint, request
from models.stories import Story

stories_bp = Blueprint("stories", __name__)
api = Api(stories_bp)


# schema for Story serialization
class StorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Story


# Story resource for getting a single story
class StoryResource(Resource):
    def get(self, story_id):
        story = Story.query.get(story_id)
        if not story:
            return {"message": "Story not found"}, 404
        result = StorySchema().dump(story)
        return result

    # PUT operation to update a story
    def put(self, story_id):
        story = Story.query.get(story_id)
        if not story:
            return {"message": "Story not found"}, 404

        data = request.get_json()
        story_schema = StorySchema()
        updated_story = story_schema.load(data, instance=story)
        db.session.commit()
        return story_schema.dump(updated_story)

    # DELETE operation to delete a story
    def delete(self, story_id):
        story = Story.query.get(story_id)
        if not story:
            return {"message": "Story not found"}, 404
        db.session.delete(story)
        db.session.commit()
        return {"message": "Story deleted"}, 204


# StoryList resource for creating new stories and viewing all stories
class StoryListResource(Resource):
    def get(self):
        stories = Story.query.all()
        result = StorySchema(many=True).dump(stories)
        return result

    def post(self):
        data = request.get_json()
        story_schema = StorySchema()
        story = story_schema.load(data)
        db.session.add(story)
        db.session.commit()
        return story_schema.dump(story), 201


# Adding resources to the API
api.add_resource(StoryListResource, "/stories")
api.add_resource(StoryResource, "/stories/<int:story_id>")
