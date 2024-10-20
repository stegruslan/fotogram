from fastapi import APIRouter

from posts.services import create_post, like_post, create_comment, \
    delete_comment, get_posts, get_comments, get_posts_subscribes

router = APIRouter(prefix="/posts", tags=["posts"])
router.get("/subscribes/")(get_posts_subscribes)
router.get("/{post_id}/comments/")(get_comments)
# Маршрут для получения комментариев к посту.

router.get("/")(get_posts)

router.post("/create/")(create_post)
# Маршрут для создания нового поста.

router.post("/{post_id}/like/")(like_post)
# Маршрут для добавления лайка к посту.

router.post("/{post_id}/comments/create")(create_comment)
# Маршрут для создания комментария к посту.

router.delete("/{post_id}/comments/{comment_id}")(delete_comment)
# Маршрут для удаления комментария.


