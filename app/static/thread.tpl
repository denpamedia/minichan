%from app.config import *
%import json

%thread_dict = json.loads(thread_json)

<!DOCTYPE html>
<html>
<head>
  <title>
    %if thread_dict['original_post_dict']['subject']:
        #{{thread_dict['thread']}}: {{thread_dict['original_post_dict']['subject']}} 
    %else:
        #{{thread_dict['thread']}}
    %end
  </title>
  <link href="{{css_assets}}" rel="stylesheet">
  <script src='{{js_assets}}'></script>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
</head>
<body>
<div class="container-fluid">
  <div class="row">
    <div class="col-md-4">
      <br>
      <!--Posting form-->
        <form action="/{{thread_dict['board']}}/{{thread_dict['thread']}}" method="post" class="form" role="form">
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
        %for my_board in sorted(BOARD_LIST):
            %if my_board == thread_dict['board']:
                <a href="/{{my_board}}" class="list-group-item active">{{BOARD_LIST[my_board]}}</a>
            %else:
                <a href="/{{my_board}}" class="list-group-item">{{BOARD_LIST[my_board]}}</a>
            %end
        %end
      </div>
    </div>
    <div class="col-md-8">
    <br>
      <ul class="list-group">
        <li class="list-group-item list-group-item-info">
          <h5 class="list-group-item-heading"><strong>
          %if thread_dict['original_post_dict']['bump_limit'] == True:
              <span class="label label-danger">Bump limit</span>
          %end
          {{thread_dict['original_post_dict']['subject']}}</strong><small> {{thread_dict['original_post_dict']['creation_time']}}</small><a name="{{thread_dict['original_post_dict']['post_id']}}" href="{{thread_dict['original_post_dict']['post_id']}}" data-text="&gt;&gt;{{thread_dict['original_post_dict']['post_id']}}" class="pull-right">&gt;&gt;{{thread_dict['original_post_dict']['post_id']}}</a></h5>
          <p class="list-group-item-text">{{thread_dict['original_post_dict']['body']}}</p>
        </li>
      </ul>
      <!--Thread list-->
      <ul class="list-group">
      %for reply in thread_dict['reply_list']:
        <li class="list-group-item">
          <h5 class="list-group-item-heading"><strong>{{reply['subject']}}</strong><small> {{reply['creation_time']}}</small><a name="{{reply['post_id']}}" href="" data-text="&gt;&gt;{{reply['post_id']}}" class="pull-right">&gt;&gt;{{reply['post_id']}}</a></h5>
          <p class="list-group-item-text">
            %for string in reply['body'].split('\n'):
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
   $("#body").val(value+" "+$(this).attr("data-text"));
   return false;
})</script>
</body>
</html>