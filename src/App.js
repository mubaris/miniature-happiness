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
          {this.state.data.map(element => 
            <li>{element.name} - {element.change.toFixed(3)}%</li>
          )}
        </ul>
      </div>
    );
  }
}

export default App;
