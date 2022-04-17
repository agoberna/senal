import React from 'react';
import BarWave from 'react-cssfx-loading/lib/BarWave';

export const Loading = (props) => {
  return (
  <div className="fill d-flex flex-column justify-content-center align-items-center">
    <p>Processing Files</p>
    <BarWave />
  </div>);
};

export default Loading;