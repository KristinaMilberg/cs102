<!DOCTYPE html>
<html>
<head>
    <title>Interesting Articles</title>
    <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
</head>
<body>
    <div class="ui container" style="padding-top: 10px;">
        <a href="javascript:history.go(-1)" class="ui primary button">Назад</a> <!-- кнопка "Назад" -->
        <h1>Возможно, вам понравятся эти статьи</h1>
        <table class="ui celled table">
            <thead>
                <th>Статьи</th>
                <th>Авторы</th>
                <th>Метки</th>
            </thead>
            <tbody>
                %for row in rows:
                <tr>
                    <td><a href="{{ row.url }}">{{ row.title }}</a></td>
                    <td>{{ row.author }}</td>
                    <td>{{ row.label }}</td>
                </tr>
                %end
            </tbody>
        </table>
    </div>
</body>
</html>