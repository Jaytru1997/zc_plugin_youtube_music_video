from rest_framework import serializers


class SongSerializer(serializers.Serializer):

    _id = serializers.CharField(read_only=True)
    plugin_id = serializers.CharField(read_only=True)
    organization_id = serializers.CharField(required=False)
    collection_name = serializers.CharField(read_only=True)
    room_id = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    duration = serializers.CharField(required=False)
    albumcover = serializers.CharField(required=False)
    url = serializers.CharField(required=False)
    userId = serializers.CharField(max_length=100, required=False)
    addedBy = serializers.CharField(required=False)
    likedBy = serializers.ListField(
        child=serializers.CharField(max_length=128), required=False, default=[]
    )
    time = serializers.IntegerField(required=False)


class LikeSongSerializer(serializers.Serializer):
    song_id = serializers.CharField(max_length=100)
    memberId = serializers.CharField(max_length=100)


class SongLikeCountSerializer(serializers.Serializer):

    songId = serializers.CharField(max_length=100)
    userId = serializers.CharField(max_length=100)


class EmojiSerializer(serializers.Serializer):  # for the emojis

    name = serializers.CharField(max_length=256, required=False)
    emoji = serializers.CharField(max_length=256, required=False)
    count = serializers.IntegerField(default=0, required=False)


class BlockSerializer(serializers.Serializer):  # for the block

    data = serializers.DictField(
        child=serializers.CharField(max_length=128),
        allow_empty=True,
        required=False,
        default={},
    )
    depth = serializers.IntegerField(default=0, required=False)
    entityRanges = serializers.ListField(
        child=serializers.CharField(max_length=128),
        allow_empty=True,
        required=False,
        default=[],
    )
    inlineStyleRanges = serializers.ListField(
        child=serializers.CharField(max_length=128),
        allow_empty=True,
        required=False,
        default=[],
    )
    key = serializers.CharField(max_length=256, required=False)
    text = serializers.CharField(max_length=256, required=False)
    type = serializers.CharField(max_length=256, required=False)


class UiDataSerializer(serializers.Serializer):  # for the ui data

    blocks = serializers.ListField(
        child=BlockSerializer(), required=False, allow_empty=True, default=[]
    )

    entityMap = serializers.DictField(
        child=serializers.CharField(max_length=128),
        allow_empty=True,
        required=False,
        default={},
    )


class CommentSerializer(serializers.Serializer):  # for the chat

    _id = serializers.CharField(read_only=True)
    plugin_id = serializers.CharField(required=False)
    organization_id = serializers.CharField(required=False)
    collection_name = serializers.CharField(required=False)
    room_id = serializers.CharField(required=False)
    username = serializers.CharField(max_length=256, required=False)
    userId = serializers.CharField(max_length=100, required=False)
    emojies = serializers.ListField(
        required=False, allow_empty=True, default=[], child=EmojiSerializer()
    )
    richUiData = UiDataSerializer(required=False, allow_null=True)
    imageUrl = serializers.CharField(max_length=256, required=False)
    time = serializers.IntegerField(required=False)


class RoomSerializer(serializers.Serializer):

    _id = serializers.CharField(read_only=True)
    room_name = serializers.CharField(max_length=100, required=False)
    plugin_name = serializers.CharField(max_length=300, required=False)
    plugin_id = serializers.CharField(max_length=300, required=False)
    organization_id = serializers.CharField(max_length=300, required=False)
    collection_name = serializers.CharField(max_length=300, required=False)
    description = serializers.CharField(max_length=300, required=False)
    created_by = serializers.CharField(max_length=100, required=False)
    is_private = serializers.BooleanField(default=False, required=False)
    is_archived = serializers.BooleanField(default=False, required=False)
    memberId = serializers.ListField(
        child=serializers.CharField(max_length=128), required=False, default=[]
    )


class AddToRoomSerializer(serializers.Serializer):
    room_id = serializers.CharField(max_length=100)
    memberId = serializers.ListField(
        child=serializers.CharField(max_length=100), allow_empty=False, default=[]
    )


class RemoveUserSerializer(serializers.Serializer):
    room_id = serializers.CharField(max_length=100)
    org_id = serializers.CharField(max_length=100)
    memberId = serializers.CharField(max_length=100)


class DeleteSongSerializer(serializers.Serializer):
    _id = serializers.CharField(max_length=100)


class DeleteChatSerializer(serializers.Serializer):
    _id = serializers.CharField(max_length=100)
