import './App.css';
import FileUpload from './components/FileUpload';
import React, { useState, useEffect } from 'react';
import TextUpload from './components/TextUpload';
import Loading from './components/Loading';
import axios from 'axios';
import Outputs from './components/Outputs';

const App = () => {
    const [pageControls, setPageControls] = useState({onHome: true, onLoad: false, onOutput: false});
    const [dataOutput, setDataOutput] = useState({});
    const [programData, setProgramData] = useState({});
    var onLoad = pageControls['onLoad'];
    const axiosInstance = axios.create({baseURL:process.env.REACT_APP_API_URL})
    // Fetch output when onLoad is changed to true
    useEffect(() => {
        const getOutput = async () => {
            if(!onLoad) return;
            try{
                const res = await axiosInstance.get('/output', {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                    params: {
                        ...programData
                    }
                });
                var myOutput = res.data;
                setDataOutput((prevState) => ({...myOutput}));
                setPageControls((prevState) => ({...(prevState), onLoad: false, onOutput: true}));
            }catch(err) {
                console.log(err);
            }
        }
        getOutput()}, [onLoad, programData, axiosInstance]); 
    return (
    <div className='container mt-4'>
        <p className="h4 display-4 text-center mb-4 top">SE&#209;AL</p>
        {pageControls['onHome'] && (
        <div>
            <div className='row mb-4'>
                <FileUpload setControls = {setPageControls} controls = {pageControls} data = {programData} setData = {setProgramData}/>
            </div>
            <div className='row'>
                <TextUpload  setControls = {setPageControls} controls = {pageControls} data = {programData} setData = {setProgramData}/>
            </div>
        </div>)}
        {pageControls['onLoad'] && (<Loading />)}
        {pageControls['onOutput'] && 
            (<Outputs setControls = {setPageControls} controls = {pageControls} data = {programData} setData = {setProgramData} output = {dataOutput}/>)}
        <div className="row">
         
        </div>
    </div>);
}

export default App;
