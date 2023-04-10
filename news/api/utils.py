from django.db import connection

from .models import Comment, News


def get_news_list(limit=10, offset=0):
    sql = """
        with news as (
            select * from api_news
            order by api_news.published desc
            limit %(limit)s
            offset %(offset)s
        )
        select news.id, news.title, news.text, news.likes, news.published,
        news.author_id, com.id, com.text, com.published, com.author_id,
        com.count from news
            left join lateral (
                select *, count(*) OVER (PARTITION BY news_id)
                from api_comment as comment
                where comment.news_id = news.id
                order by comment.published desc
                limit 10
                ) as com on true
    """ % {'limit': limit, 'offset': offset}
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()

    return _get_instances(rows)


def get_news_object(obj_pk):
    sql = """
        select news.id, news.title, news.text, news.likes, news.published,
        news.author_id, com.id, com.text, com.published, com.author_id,
        com.count from api_news news
            left join lateral (
                select *, count(*) OVER (PARTITION BY news_id)
                from api_comment as comment
                where comment.news_id = news.id
                order by comment.published desc
                limit 10
                ) as com on true
        where news.id = %(pk)s
    """ % {'pk': obj_pk}
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()

    news_list = _get_instances(rows)
    if not news_list:
        return
    return news_list[0]


def _get_instances(rows):
    news_items = {}
    for (
            news_id, news_title, news_text, news_likes, news_published,
            news_author_id, com_id, com_text, com_published,
            com_author_id, num_comments
    ) in rows:
        news_fields = (news_id, news_title, news_text, news_likes,
                       news_published, news_author_id, num_comments)
        if com_id is None:
            news_items[news_fields] = []
            continue
        comments = news_items.get(news_fields)
        comment_instance = Comment(
            id=com_id, text=com_text, author_id=com_author_id,
            published=com_published
        )
        if comments is None:
            news_items[news_fields] = [comment_instance]
        else:
            news_items[news_fields].append(comment_instance)

    news = []
    for key, comments_list in news_items.items():
        news_id, title, text, likes, published, author_id, num_comments = key
        news_instance = News(id=news_id, title=title, text=text, likes=likes,
                             author_id=author_id, published=published)
        news_instance.num_comments = (0 if num_comments is None
                                      else num_comments)
        news_instance.comments_ = comments_list
        news.append(news_instance)
    return news
