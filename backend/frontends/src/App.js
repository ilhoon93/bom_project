import React, { Component } from 'react';







class App extends Component {

  state = {
    todos: []
  };
  async componentDidMount() {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/bar_skin');
      const todos = await res.json();
      this.setState({
        todos
      });
    } catch (e) {
      console.log(e);
    }
  }
  render() {
    return (

      <div>
        {this.state.todos.map(item => (
          <div>
            <h1>{item.skin_type}</h1>
            <span>{item.count}</span>
          </div>
        ))}
      </div>
    );
  }
}

export default App;



// import React, { Component } from 'react';
// import logo from './logo.svg';
// import './App.css';

// class App extends Component {
//   render() {
//     return (
//       <div className="App">
//         <header className="App-header">
//           <img src={logo} className="App-logo" alt="logo" />
//           <h1 className="App-title">Welcome to React</h1>
//         </header>
//         <p className="App-intro">
//           To get started, edit <code>src/App.js</code> and save to reload.
//         </p>
//       </div>
//     );
//   }
// }

// export default App;
