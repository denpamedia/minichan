<!DOCTYPE html>
<html>
<head>
  <title>Minichan/{{board}}/{{thread_number}}</title>
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
      <form action="/{{board}}/{{thread_number}}" method="post" class="form" role="form">
        <div class="input-group">
          <input type="text" name="subject" class="form-control" maxlength="50" placeholder="Subject">
            <span class="input-group-btn">
              <button class="btn btn-primary" type="submit">Submit</button>
            </span>
        </div>
          <br>
          <textarea name="body" id="body" class="form-control" maxlength="3000" rows="4" required></textarea>
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
      <!--End of board list-->
    </div>
    <div class="col-md-8">
      <br>
      <ul class="list-group">
        <li class="list-group-item list-group-item-info">
          <h5 class="list-group-item-heading"><strong>{{thread.subject}}</strong><small> {{thread.creation_time}}</small><a name="{{thread.post_id}}" href="{{thread.post_id}}" data-text="&gt;&gt;{{thread.post_id}}" class="pull-right">&gt;&gt;{{thread.post_id}}</a></h5>
          <p class="list-group-item-text">{{thread.body}}</p>
        </li>
      </ul>
      <!--Reply list-->
      <ul class="list-group">
      %for reply in reply_list:
        <li class="list-group-item">
          <h5 class="list-group-item-heading"><strong>{{reply.subject}}</strong><small> {{reply.creation_time}}</small><a name="{{reply.post_id}}" href="" data-text="&gt;&gt;{{reply.post_id}}" class="pull-right">&gt;&gt;{{reply.post_id}}</a></h5>
          <p class="list-group-item-text">
            %for string in reply.body.split('\n'):
                %for word in string.split():
                    %if word.startswith('>>') and word[2:].isdigit():
                        <a href="#{{word[2:]}}">{{word}} </a>
                    %else:
                        {{word}}
                    %end
                %end
            <br>
            %end
          </p>
        </li>
        %end
      </ul>
      <!--End of thread list-->
    </div>
  </div>
</div>

  <script>$("a[data-text]").click(function(){
  var value = $("#body").val();
   $("#body").val(value+$(this).attr("data-text"));
   return false;
})</script>
</body>
</html>