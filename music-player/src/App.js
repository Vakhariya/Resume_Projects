import {useState, useEffect} from 'react';
import Player from './Components/Player';


function App() {
  const [songs] = useState([
    {
      title: "Dhadak Title Song",
      artist: "Ajay-Atul && Shreya Ghosal",
      img_src: "./images/Dhadak.jpg",
      src: "./music/Dhadak.mp3"
    },
    {
      title: "Mai Nikla Gaddi Leke",
      artist: "Aditya Narayan, Mithoon &&  Udit Narayan",
      img_src: "./images/Main_Nikla_Gaddi_Leke.jpg",
      src: "./music/Mai_Nikla_Gaddi_Leke.mp3"
    },
    {
      title: "Galla Goodiyaan",
      artist: "Javed Akhtar && Farhan Akhtar",
      img_src: "./images/Galla_Goodiyaan.jpg",
      src: "./music/Gallan_Goodiyaan.mp3"
    },
    {
      title: "Chogada Tara",
      artist: "Asees Kaur && Darshan Raval",
      img_src: "./images/Chogada.jpeg",
      src: "./music/Chogada.mp3"
    }
  ]);

  const [currentSongIndex, setCurrentSongIndex] = useState(0);
  const [nextSongIndex, setNextSongIndex] = useState(0);

  useEffect(() => {
    setNextSongIndex(() => {
      if (currentSongIndex + 1 > songs.length - 1) {
        return 0;
      } else {
        return currentSongIndex + 1;
      }
    });
  }, [currentSongIndex]);

  return (
    <div className="App">
      <Player 
        currentSongIndex={currentSongIndex} 
        setCurrentSongIndex={setCurrentSongIndex} 
        nextSongIndex={nextSongIndex} 
        songs={songs}
      />
    </div>
  );
}

export default App;