var Comment = React.createClass({
  render: function() {
    return (
      <tr>
        <td>{this.props.ranking}</td>
        <td>{this.props.wowclass}</td>
        <td>{this.props.race}</td>
        <td>{this.props.name}</td>
        <td>{this.props.rating}</td>
      </tr>
    );
  }
});

var CommentBox = React.createClass({
  callToPass: function(d) {
    if (d != this.state.date_filter && d != []) {
      this.state.date_filter = d;
      //this.setState({date_filter: d});
      console.log("pls call me bb");
      console.log(d);
      console.log(this.state);
      this.loadCommentsFromServer();
    }
  },
  loadDatesFromServer: function() {
    console.log("loadDatesFromServer");
    $.ajax({
      url: '/dates/',
      success: function(data) {
        console.log("loadDatesFromServer.returned");
        this.setState({dates: data});
        this.setState({date_filter: data[0]});
        this._child.pickFirst();
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  loadCommentsFromServer: function() {
    console.log("DATA:");
    console.log(this.state.date_filter);
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
    console.log("CommentBox.CDM");
    this.loadCommentsFromServer();
    this.loadDatesFromServer();
  },
  render: function() {
    console.log("CommentBox.render");
    return (
      <div className="container">
      <div className="col-md-2"></div>
      <div className="col-md-8 commentBox">
        <CommentDateSelect ref={(child) => {this._child=child; }} data={this.state.dates} callme={this.callToPass}/>
        <CommentList data={this.state.data} />
      </div>
      <div className="col-md-2"></div>
      </div>
    );
  }
});

var CommentDateSelect = React.createClass({
  getInitialState: function() {

    return {selected: []};
  },
  pickFirst: function() {
    this.setState({selected: $('.dropdown-menu li a').first().text()});
  },
  render: function() {
    console.log("CommentDateSelect.render");
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
    console.log("CommentDateSelect.componentDidUpdate");
    this.props.callme(this.state.selected);
  },
});

var CommentList = React.createClass({
  render: function() {
    var commentNodes = this.props.data.map(function(comment) {
      return (
        <Comment wowclass={comment.class} ranking={comment.ranking} race={comment.race} key={comment.id} name={comment.name} rating={comment.rating}>
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
        <th>Name</th>
        <th>Rating</th>
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
