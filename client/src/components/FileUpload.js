import React, { Fragment, useState } from 'react';
import axios from 'axios';

export const FileUpload = (props) => {
  const [file, setFile] = useState('');
  const [vocab, setVocab] = useState('');
  const allPrograms = ['Synt Analysis', 'Lex Analysis', 'Grammar Assistant', 'L2 Classifier'];
  const axiosInstance = axios.create({baseURL:process.env.REACT_APP_API_URL})

  const onChange = e => {
    setFile(e.target.files[0]);
  }

  const onChangeVocab = e => {
    setVocab(e.target.files[0]);
  }

  const onChangeProgram = (e, program) => {
    if(program === "all"){
      props.setData(prevState => ({...(prevState), program: allPrograms}));
    }
    else{
      props.setData(prevState => ({...(prevState), program: [program]}));
    }
  }

  const onSubmit = async e => {
      e.preventDefault();
      const formData = new FormData();
      formData.append('file', file);
      formData.append('vocab', vocab);

      try {
        const res = await axiosInstance.post('/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });

        const { fileName, filePath} = res.data;

        props.setData(prevState => ({...(prevState), name: fileName, path: filePath}));
        props.setControls((prevState) => ({...(prevState), onHome: false, onLoad: true}));


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
                    <p className="col-md-8 offset-md-2 text-center">To use the SYNT Analyzer, LEX Analyzer, Grammar Assistant, and full-text L2 Classifier, please select a file from your file explorer and click your desired output from the buttons below.</p>
                </div>
                <div className="custom-file row">
                  <div className='container d-flex'>
                    <button type="button" class="btn btn-secondary btn-sm" disabled>File to be Analyzed</button>
                    <input type="file" className="col form-control formElement" id="customFile" onChange={onChange}/>
                  </div>
                </div>
                <div className="row">
                    <p className="col-md-8 offset-md-2 text-center pt-3">If you will be using the Grammar Assistant, and would like to track your own vocabulary list, please upload it below.</p>
                </div>
                <div className="custom-file row mb-0 pb-0">
                  <div className='container d-flex'>
                    <button type="button" class="btn btn-secondary btn-sm" disabled>Vocabulary List</button>
                    <input type="file" className="col form-control formElement" id="customVocab" onChange={onChangeVocab}/>
                  </div>
                </div>
                <div className="row my-3">
                    <div className="col px-0">
                        <input 
                          type="submit" 
                          value="Synt Analysis" 
                          name="synt"
                          className="btn btn-primary w-100" 
                          onClick= {e => onChangeProgram(e, "Synt Analysis")}
                        />
                    </div>
                    <div className="col px-0">
                        <input 
                          type="submit" 
                          value="Lex Analysis" 
                          name="lex"
                          className="btn btn-primary w-100"
                          onClick= {e => onChangeProgram(e, "Lex Analysis")} 
                        />
                    </div>
                    <div className="col px-0">
                        <input 
                          type="submit" 
                          name="grammar"
                          value="Grammar Assistant" 
                          className="btn btn-primary w-100" 
                          onClick= {e => onChangeProgram(e, "Grammar Assistant")}
                        />
                    </div>
                    <div className="col px-0">
                        <input 
                          type="submit" 
                          name="l2classifier"
                          value="L2 Classifier" 
                          className="btn btn-primary w-100" 
                          onClick= {e => onChangeProgram(e, "L2 Classifier")}
                        />
                    </div>

                </div>
                {/*<div className="row">
                    <input 
                      name="all"
                      type="submit" 
                      value="Run All" 
                      className="btn btn-primary" 
                      onClick= {e => onChangeProgram(e, "all")}
                    />
                </div>*/}
            </div>
        </form>
      </Fragment>
  );
};

export default FileUpload;