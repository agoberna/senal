import React from 'react';
import Plot from 'react-plotly.js';

export const Outputs = (props) => {
  const displayRow = (rowData, i) => {
    if(i === 0){
      return;
    }
    return (
    <tr>
      <td>{i}</td>
      {rowData.map((cellData) => <td>{cellData}</td>)}
    </tr>)
  }
  const showTable = (tableData) => {
    let tableTitle = tableData["title"]
    return (
    <div className='col pt-3'>
      <h6 className='text-center'>{tableTitle}</h6>
      <table>
        <thead>
          <tr>
            <th></th>
            {tableData["data"][0].map((headerName, i) => <th>{headerName}</th>)}
          </tr>
        </thead>
        <tbody>
          {tableData["data"].map((rowData, i) => displayRow(rowData, i))}
        </tbody>
      </table>
    </div>)
  }
  const mapArrayToDisplayBoxplotData = (dataArray) => {
    return {
      y: dataArray[1],
      type: 'box',
      name: dataArray[0],
      marker: {
        color: 'rgb(107,174,214)'
      },
      boxpoints: 'Outliers'
    }
  }
  const showBoxplot = (boxplotData) => {
    let boxplotDisplayData = boxplotData["data"].map((dataArray) => mapArrayToDisplayBoxplotData(dataArray));
    let boxplotTitle = boxplotData["title"];
    return (
      <div className='col mx-auto d-flex align-items-center justify-content-center'>
        <Plot
          data={boxplotDisplayData}
          layout={ {title: boxplotTitle}}
        />
      </div>
    )
  }
  const barDataToTrace = (dataArray) => {
    return {
      x: (dataArray['x-value']),
      y: (dataArray['y-value']),
      type: 'bar',
      marker: {
        color: 'rgb(158,202,225)',
        opacity: 0.6,
        line: {
          color: 'rgb(8,48,107)',
          width: 1.5
        }
      }
    }
  }
  const showBar = (barData) => {
    let barDisplayData = barDataToTrace(barData["data"]);
    let barTitle = barData["title"];
    return (
      <div className='col mx-auto dataElement pr-4'>
        <Plot
          data={[barDisplayData]}
          layout={ {title: barTitle} }
          className='setLeft'
        />
      </div>
    )
  }

  const pieDataToTrace = (dataArray) => {
    return {
      type: "pie",
      values: dataArray['totals'],
      labels: dataArray['labels'],
      textinfo: "label+percent",
      textposition: "outside",
      automargin: true
    }
  }

  const showPie = (pieData) => {
    let pieDisplayData = pieDataToTrace(pieData["data"]);
    let pieTitle = pieData["title"];
    return (
      <div className='col mx-auto dataElement pr-4'>
        <Plot
          data={[pieDisplayData]}
          layout={ {title: pieTitle} }
          className='setLeft'
        />
      </div>
    )
  }

  const showDataElement = (program, data) => {
    if(data === 'table'){
      return (props.output[program][data]).map(showTable);
    }
    else if(data === 'boxplot'){
      return (props.output[program][data]).map(showBoxplot);
    }
    else if(data === 'bar'){
      return (props.output[program][data]).map(showBar);
    }
    else if(data === 'pie'){
      return (props.output[program][data]).map(showPie);
    }
  }
  const showData = (program) => {
    const outputByProgram = Object.keys(props.output[program]);
    return (
    <div className='row pt-4 justify-content-center align-items-center'>
      {outputByProgram.map((data) => (showDataElement(program, data)))}
    </div>)
  }
  const returnToHome = () => {
    props.setControls((prevState) => ({...(prevState), onOutput: false, onHome: true}));
  }
  const setOptions = (prog, i) => {
    return (<option key = {prog}>{prog + ' Output'}</option>);
  }
  const changeOutput = (e) => {
    // Set state to show proper output
  }

  const outputArray = Object.keys(props.output);
  const defaultSelection = props.data['program'][0] + ' Output';
  return (
  <div className="fill d-flex flex-column align-items-center p-0 m-0">
    <div className="row w-100">
      <div className='col'>
        <select className="form-select mb-3" aria-label=".form-select-lg example" onChange={changeOutput} defaultValue = {defaultSelection}>
          {
            props.data['program'].map((prog, i) => (setOptions(prog, i)))
          }
        </select>
      </div>
      <div className='col'>
      </div>
      <div className='col'>
      </div>
      <div className='col'>
        <input type="button" className="btn-rounded btn btn-danger btn-block w-100 justify-content-end" value="Analyze More Files" onClick={e => returnToHome()}/>
      </div>
    </div>
    {outputArray.map((program) => (showData(program)))}
  </div>);
};

export default Outputs;