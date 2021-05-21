import React, { Component } from 'react';
import { render } from 'react-dom';
import LineChart from './LineChart';
const aHashData = require('./data/aHash.json');
const dHashData = require('./data/dHash.json');
const pHashData = require('./data/pHash.json');

class App extends Component {
  
  constructor() {
    super();
    
  }
  render(){
    console.log(aHashData);
    return (<div>
      <LineChart name="Average Hash" data={aHashData}/>
      <LineChart name="Difference Hash" data={dHashData}/>
      <LineChart name="Perceptual Hash" data={pHashData}/>
    </div>)
  }
}

render(<App />, document.getElementById('root'));
