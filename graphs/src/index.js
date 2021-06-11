import React, { Component } from 'react';
import { render } from 'react-dom';
import LineChart from './LineChart';
const aHashData = require('./data/aHash.json');
const dHashData = require('./data/dHash.json');
const pHashData = require('./data/pHash.json');
const wHashData = require('./data/whash.json');

class App extends Component {
  
  constructor() {
    super();
    
  }

  runner(data,name){
    return (<div>
      <LineChart name={name + " Level 1"} data={{"Level 1" : aHashData["Level 1"]}}/>
      <LineChart name={name + " Level 2"} data={{"Level 2" : aHashData["Level 2"]}}/>
      <LineChart name={name + " Level 3"} data={{"Level 3" : aHashData["Level 3"]}}/>
    </div>)
  }

  render(){
    console.log(aHashData);
    return (<div>
      {this.runner(aHashData,"Average Hash")}
      {this.runner(dHashData,"Difference Hash")}
      {this.runner(pHashData,"Perceptual Hash")}
      {this.runner(wHashData,"Wavelet Hash")}
      {/* <LineChart name="Difference Hash" data={dHashData}/>
      <LineChart name="Perceptual Hash" data={pHashData}/>
      <LineChart name="Wavelet Hash" data={wHashData}/> */}
    </div>)
  }
}

render(<App />, document.getElementById('root'));
