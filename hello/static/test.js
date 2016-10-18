var Comment = React.createClass({
  render: function() {
    return (
      <tr>
        <td>{this.props.ranking}</td>
        <td>{this.props.wowclass}</td>
        <td>{this.props.race}</td>
      </tr>
    );
  }
});

var CommentBox = React.createClass({
  callToPass: function(d) {
    if (d != this.state.date_filter) {
      this.state.date_filter=d;
      console.log("pls call me bb");
      console.log(d);
      this.loadCommentsFromServer();
    }
  },
  loadDatesFromServer: function() {
    $.ajax({
      url: '/dates/',
      success: function(data) {
        this.setState({dates: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  loadCommentsFromServer: function() {
    $.ajax({
      url: '/data/',
      data: this.state.date_filter!=""?{pull_date: this.state.date_filter}:{},
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  getInitialState: function() {
    return {data: [], dates: [], date_filter: ""};
  },
  componentDidMount: function() {
    this.loadCommentsFromServer();
    this.loadDatesFromServer();
  },
  render: function() {
    return (
      <div className="commentBox">
        <CommentDateSelect data={this.state.dates} callme={this.callToPass}/>
        <CommentList data={this.state.data} />
      </div>
    );
  }
});

var CommentDateSelect = React.createClass({
  getInitialState: function() {
    return {selected: []};
  },
  render: function() {
    var dateChoices = this.props.data.map(function(date) {
      return (
        <li><a href="#">{date}</a></li>
      );
    });
    return (
      <div className="dropdown">
      <button className="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown" >Pull Date {this.state.selected}
      <span className="caret"></span></button>
      <ul className="dropdown-menu" onClick={this.handleClick}>
        {dateChoices}
      </ul>
    </div>
    );
  },
  handleClick: function(e) {
    this.setState({selected: e.target.innerHTML});
  },
  componentDidUpdate: function() {
    console.log("C_DID_UPDATE")
    this.props.callme(this.state.selected)
  },
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
      <table className="table">
      <thead>
      <tr>
        <th>Rank</th>
        <th>Class</th>
        <th>Race</th>
      </tr>
    </thead>
    <tbody>
        {commentNodes}
        </tbody>
      </table>
    );
  }
});

ReactDOM.render(
  <CommentBox url="/data/" />,
  document.getElementById('content')
);
