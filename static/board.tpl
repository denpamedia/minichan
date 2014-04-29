<!DOCTYPE html>
<html>
<head>
  <title>Minichan/{{board}}</title>
  <link href="/static/css/bootstrap.min.css" rel="stylesheet">
  <link href="/static/css/mystyle.css" rel="stylesheet">
  <script src='/static/js/jquery.js'></script>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
</head>
<body>
<div class="container-fluid">
  <div class="row">
    <div class="col-md-4">
      <br>
      <!--Posting form-->
      <form action="/{{board}}" method="post" class="form" role="form">
        <div class="input-group">
          <input type="text" name="subject" class="form-control" maxlength="50" placeholder="Subject">
            <span class="input-group-btn">
              <button class="btn btn-primary" type="submit">Submit</button>
            </span>
        </div>
          <br>
          <textarea type="text" name="body" class="form-control" maxlength="3000" rows="4" required></textarea>
      </form>
      <!--End of posting form-->
      <br>
      <!--Board list-->
      <div class="list-group">
        <label>Boards</label>
        %for my_board in sorted(board_list):
            %if my_board == board:
                <a href="/{{my_board}}" class="list-group-item active">{{board_list[my_board]}}</a>
            %else:
                <a href="/{{my_board}}" class="list-group-item">{{board_list[my_board]}}</a>
            %end
        %end
      </div>
    </div>
    <div class="col-md-8">
      <!--End of board list-->
      <br>
      <!--Thread list-->
      %for thread in thread_list:
      <div class="list-group">
        <a href="/{{board}}/{{thread.post_id}}" class="list-group-item list-group-item-info">
          <h5 class="list-group-item-heading"><strong><span class="badge">{{thread.bump_counter}}</span> {{thread.subject}}</strong><small> {{thread.creation_time}}</small><span class="pull-right">&gt;&gt;{{thread.post_id}}</span></h5>
          <p class="list-group-item-text">
          %if len(thread.body) >= 1000:
              %for string in thread.body[:1000].split('\n'):
                  {{string}}<br>
              %end
              [...]
          %else:
              %for string in thread.body.split('\n'):
                  {{string}}<br>
              %end
          %end
          </p>
        </a>
      </div>
      %end
      <!--End of thread list-->
    </div>
  </div>
</div>
</body>
</html>