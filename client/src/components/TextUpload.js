import React, { Fragment, useState} from 'react';
import axios from 'axios';
import BarWave from 'react-cssfx-loading/lib/BarWave';


export const TextUpload = (props) => {
  const [outputData, setOutputData] = useState({});
  const [program, setProgram] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const axiosInstance = axios.create({baseURL:process.env.REACT_APP_API_URL})

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

  const onChangeProgram = (e, program) => {
    props.setData(prevState => ({...(prevState), program: [program]}));  
    setProgram(program);
    setOutputData({});
  }

  const onSubmit = async e => {
    e.preventDefault();

    let text = document.getElementById('customText').value;
    setIsLoading(true);

    try {
      const res = await axiosInstance.get('/textOutput', {
        headers: {
            'Content-Type': 'multipart/form-data'
        },
        params: {
            text : text,
            program: program
        }
      });
      setIsLoading(false);
      setOutputData((prevState) => ({...(res.data)}));
    }catch(err) {
      if(err.response.status === 500){
          console.log('There was a problem with the server')
      } else{
          console.log(err.response.data.msg);
      }
    }
  }
  return  (
      <Fragment>
        <form onSubmit={onSubmit}>
            <div className='container'>
                <div className="row">
                    <p className="col-md-8 offset-md-2 text-center">To use CAPTURA and the L2 Classifier on specific inputs, please copy/paste the target phrase(s) and click your desired output from the buttons below.</p>
                </div>
                <div className="custom-file row">
                    <input type="text" className="form-control" id="customText" placeholder="Paste text here"/>
                </div>
                <div className="row my-1">
                    <div className="col px-0">
                        <input 
                          type="submit" 
                          value="L2 Classifier" 
                          name="l2classifiertext"
                          className="btn btn-primary w-100" 
                          onClick= {e => onChangeProgram(e, "Text L2 Classifier")}
                        />
                    </div>
                    <div className="col px-0">
                        <input 
                          type="submit" 
                          value="CAPTURA" 
                          name="captura"
                          className="btn btn-primary w-100"
                          onClick= {e => onChangeProgram(e, "CAPTURA")} 
                        />
                    </div>
                </div>
            </div>
        </form>
        <div className="d-flex flex-column align-items-center p-0 m-0 small">
          <div className="row w-100 small" >
            {(Object.keys(outputData).length > 0) && 
            (<div className='col'>
              {(outputData[Object.keys(outputData)]['table'].map(showTable))}
            </div>)}
            {isLoading && 
            (<div className='col d-flex flex-column justify-content-center align-items-center'>
              <p>Processing Text</p>
              <BarWave />       
            </div>)}
          </div>
        </div>
      </Fragment>
);
};

export default TextUpload;