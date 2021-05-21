import React from 'react';
import { Line } from 'react-chartjs-2';
const randomColor = require('randomcolor');


const makeData = (dataSet, name) => {
    let label = [];
    let data = [];
    for(let level in dataSet){
        console.log("level",dataSet[level])
        for(let key in dataSet[level]){
            label.push(dataSet[level][key][0]);
        }
        break;
    }
    let result = {
        labels : label,
        datasets : null
    }
    for(let level in dataSet){
        let levelData = {
            label : level + " for " + name,
            backgroundColor: randomColor(),
            borderColor: randomColor(),
            fill : false,
            data : []
        };
        let dt = [];
        for(let key in dataSet[level]){
            dt.push(dataSet[level][key][1])
        }
        levelData.data = dt;
        data.push(levelData);
    }
    result.datasets = data;
    console.log(result);
    return result;
}


const options = {
  scales: {
    yAxes: [
      {
        ticks: {
          beginAtZero: true,
        },
      },
    ],
    xAxes : [
        {
            ticks : {
                beginAtZero : true,
            },
            reverse : true,
        },
    ],
  },
};



const LineChart = (props) => {
    console.log("props", props)
    return (<div>
        <div className='header'>
        <h1 className='title'>{props.name}</h1>
        </div>
        <Line data={makeData(props.data, props.name)} options={options} />
    </div>
    );
}
export default LineChart;