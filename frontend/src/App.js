import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const App = () => {
const [videoSrc, setVideoSrc] = useState('');
const [snapshots, setSnapshots] = useState([]);
const [hovering, setHovering] = useState(false);
const [paused, setPaused] = useState(true);
const [currentIndex, setcurrentIndex] = useState(0);
const [showSnapshot, setShowSnapshot] = useState(false);


useEffect(() => {
    // Fetch video source
    const fetchVideo = async () => {
    try {
        const response = await axios.get('http://localhost:8000/api/videos', {
        responseType: 'blob'
    });
        setVideoSrc(URL.createObjectURL(response.data));
    } catch (error) {
        console.error("Error fetching video:", error);
    }
};

    // Fetch snapshots
    const fetchSnapshots = async () => {
    try {
        const response = await axios.get('http://localhost:8000/api/videos/snapshots');
        setSnapshots(response.data.snapshots);
    } catch (error) {
        console.error("Error fetching snapshots:", error);
    }
};
    hovering && paused ? fetchSnapshots() : fetchVideo();
}, [hovering, paused]);

useEffect(() => {
    if (snapshots.length === 0) {
        return;
    }
    const intervalId = setInterval(() => {
        setcurrentIndex((prevIndex) => (prevIndex + 1) % snapshots.length);
    }, 90);

    return () => clearInterval(intervalId); // Cleanup interval on component unmount
}, [snapshots]);

useEffect(() => {
    let timer;
    if (hovering && paused && snapshots.length > 0) {
        timer = setTimeout(() => {
    setShowSnapshot(true);
        }, 2000);
    } else {
    setShowSnapshot(false);
        }
    return() =>clearTimeout(timer);
}, [hovering, paused, snapshots]);

const handleMouseEnter = () => {
    setHovering(true);
};

const handleMouseLeave = () => {
    setHovering(false);
};

const handlePlayPause = (event) => {
    setPaused(event.target.paused);
};

    return (
    <div className="video-container">
        {showSnapshot ? (
             <img 
                    className="video-container"
                    src={`data:image/png;base64,${snapshots[currentIndex]}`}
                    alt="Decoded Base64"
                    onMouseEnter={handleMouseEnter}
                    onMouseLeave={handleMouseLeave}
                />
            ): (<video
                src={videoSrc}
                controls
                width="600"
                onMouseEnter={handleMouseEnter}
                onMouseLeave={handleMouseLeave}
                onPlay={handlePlayPause}
                onPause={handlePlayPause}
            ></video>)}
    </div>
  );
};

export default App;
