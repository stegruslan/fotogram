from fastapi import APIRouter

from posts.services import create_post, like_post, create_comment, \
    delete_comment, get_posts, get_comments

router = APIRouter(prefix="/posts", tags=["posts"])
# Создаем экземпляр APIRouter с префиксом пути "/posts" и тегом "posts".
router.get("/{post_id}/comments/")(get_comments)
# Маршрут для получения комментариев к посту.
# Когда клиент отправляет GET-запрос на путь "/posts/{post_id}/comments/",
# вызывается функция get_comments.
router.get("/")(get_posts)
# Маршрут для получения всех постов.
# Когда клиент отправляет GET-запрос на путь "/posts/",
# вызывается функция get_posts.
router.post("/create/")(create_post)
# Маршрут для создания нового поста.
# Когда клиент отправляет POST-запрос на путь "/posts/create/",
# вызывается функция create_post.
router.post("/{post_id}/like/")(like_post)
# Маршрут для добавления лайка к посту.
# Когда клиент отправляет POST-запрос на путь "/posts/{post_id}/like/",
# вызывается функция like_post.
router.post("/{post_id}/comments/create")(create_comment)
# Маршрут для создания комментария к посту.
# Когда клиент отправляет POST-запрос на путь
# "/posts/{post_id}/comments/create", вызывается функция create_comment.
router.delete("/{post_id}/comments/{comment_id}")(delete_comment)
# Маршрут для удаления комментария.
# Когда клиент отправляет DELETE-запрос на путь
# "/posts/{post_id}/comments/{comment_id}", вызывается функция delete_comment.
