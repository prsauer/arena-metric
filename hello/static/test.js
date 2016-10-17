var Comment = React.createClass({
  render: function() {
    return (
      <div class="panel panel-default">
      <div class="panel-heading">
        <h3 class="panel-title">{this.props.ranking}</h3>
      </div>
      <div class="panel-body">
        {this.props.race} {this.props.wowclass}
      </div>
    </div>
    );
  }
});

var CommentBox = React.createClass({
  loadCommentsFromServer: function() {
    $.ajax({
      url: '/data/',
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  getInitialState: function() {
    return {data: []};
  },
  componentDidMount: function() {
    this.loadCommentsFromServer();
    setInterval(this.loadCommentsFromServer, this.props.pollInterval);
  },
  render: function() {
    return (
      <div className="commentBox">
        <h1>Comments</h1>
        <CommentList data={this.state.data} />
      </div>
    );
  }
});

var CommentList = React.createClass({
  render: function() {
    var commentNodes = this.props.data.map(function(comment) {
      return (
        <Comment wowclass={comment.class} ranking={comment.ranking} race={comment.race} key={comment.id}>
        </Comment>
      );
    });
    return (
      <div className="commentList">
        {commentNodes}
      </div>
    );
  }
});

ReactDOM.render(
  <CommentBox url="/data/" pollInterval={30000} />,
  document.getElementById('content')
);
