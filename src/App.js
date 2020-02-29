import React, {Component} from 'react';
import data from './data.json';

class App extends Component {
  state = {
    data: data
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
      </div>
    );
  }
}

export default App;
