import React,{ useEffect,useState } from 'react';
import axios from 'axios';

const Home = () => {
    const [ state,setState ] = useState()
    useEffect(()=>{
        async function getdata(params) {
            const { data } = await axios.get(`api/v1/order/`);
            setState(data)
        }getdata()
    },[])
  return (
      <div>
          {
              state && state.map(dt=>(
                  <div key={dt.id}>
                      <h1>{dt.order_status}</h1>
                  </div>
              ))
          }
      </div>    
  )
}

export default Home;