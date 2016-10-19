var RankDateContainer = React.createClass({
  render: function() {
    console.log("RankDateContainer.render");
    return (
      <div>
        <RankDateSelect dates={this.state.data}></RankDateSelect>
      </div>
    );
  },
  componentDidMount: function() {
    console.log("RankDateContainer.componentDidMount.AJAX_DATES");
    $.ajax({
      url: '/dates/',
      success: function(data) {
        console.log("AJAX_DATES.returned");
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  getInitialState: function() {
    console.log("RankDateContainer.getInitialState");
    return {data: []};
  },
});

var RankDateSelect = React.createClass({
  getInitialState: function() {
    console.log("RankDateSelect.getInitialState");
    return {selected: []};
  },
  componentWillReceiveProps: function(newProps) {
    console.log("RankDateSelect.componentWillReceiveProps");
    if (newProps.dates.length > 0) {
      this.setState({selected: newProps.dates[0]});
    }
  },
  render: function() {
    console.log("RankDateSelect.render");
    var dateChoices = this.props.dates.map(function(date) {
      return (
        <li><a href="#">{date}</a></li>
      );
    });
    return (
      <div>
        <div className="dropdown">
        <button className="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown" >Pull Date {this.state.selected}
        <span className="caret"></span></button>
        <ul className="dropdown-menu" onClick={this.handleClick}>
          {dateChoices}
        </ul>
        </div>
        <PlayerList date_filter={this.state.selected}></PlayerList>
      </div>
    );
  },
  handleClick: function(e) {
    console.log("Click");
    console.log(e.target);
    if (e.target != undefined) {
      this.setState({selected: e.target.innerHTML});
    }
  },
});

var PlayerList = React.createClass({
  getInitialState: function() {
    console.log("PlayerList.getInitialState");
    return {data: []};
  },
  componentWillReceiveProps: function(nextProps) {
    console.log("componentWillReceiveProps.AJAX_RANKS:");
    $.ajax({
      url: '/data/',
      data: nextProps.date_filter!=""?{pull_date: nextProps.date_filter}:{},
      success: function(data) {
        console.log("AJAX_RANKS.returned");
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  render: function() {
    console.log("PlayerList.render");
    var playerNodes = this.state.data.map(function(player) {
      return (
        <Player wowclass={player.class}
                ranking={player.ranking} race={player.race} key={player.id} name={player.name} rating={player.rating}>
        </Player>
      );
    });
    return (
      <table className="table">
        <thead>
          <tr>
            <th>Rank</th><th>Class</th><th>Race</th><th>Name</th><th>Rating</th>
          </tr>
        </thead>
        <tbody>{playerNodes}</tbody>
      </table>
    )
  }
});

var Player = React.createClass({
  render: function() {
    console.log("Player.render");
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

ReactDOM.render(
  <RankDateContainer />,
  document.getElementById('content')
);
