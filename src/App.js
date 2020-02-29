import React, {Component} from 'react';
import axios from 'axios';
import data from './data.json';

class App extends Component {
  state = {
    data: data
  }

  refresh() {
    axios.post("https://api.netlify.com/build_hooks/5e5a4c4067d7da3b14426f10", {})
      .then((res) => {
        console.log("Successful Refresh", res.data);
      })
      .catch((err) => {
        console.log("Error while refreshing", err);
      })
  }

  render() {
    return (
      <div className="App">
        <ul>
          {this.state.data.data.map(element => 
            <li>{element.name} - {element.change.toFixed(3)}%</li>
          )}
        </ul>
          <span>Last Updated - {this.state.data.date}</span>
          <button onClick={this.refresh.bind(this)}>Refresh</button>
      </div>
    );
  }
}

export default App;
