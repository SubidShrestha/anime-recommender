import React from 'react';
import { useState } from 'react';
import axios from 'axios';

export const Home = () => {
    const [anime,setAnime] = useState('');
    const [recommendation, setRecommendation] = useState([]);
    const [btnTxt,setBtnText] = useState('Get Suggestions');
    const [btnStatus,setBtnStatus] = useState(false);

    const fetchAnimeResults = async(e) => {
        e.preventDefault();
        if ((anime === '')||(anime === null)){
            alert('Need to give an appropriate anime name.');
            return;
        }
        try{
            setBtnText('Getting Suggestions')
            setBtnStatus(true)
            const animeData = await axios.post('http://127.0.0.1:5000/api/anime/',{
                title : anime
            })
            setRecommendation(animeData.data)
            setBtnText('Get Suggestions')
            setBtnStatus(false)
        }catch(err){
            console.log(err);
        }
    }
    return (
        <>
            <div className="flex flex-col items-center relative min-h-screen bg-gray-800 text-white">
                <div className="w-4/5 mx-auto">
                    <h2 className="font-rosarivo font-bold text-2xl text-center pt-20 pb-6">
                        Anime Recommendation
                    </h2>
                    <h3 className="font-rosarivo font-bold uppercase tracking-wide mb-12 text-base px-4 text-center">
                        Get anime suggestion based on your favorite anime
                    </h3>
                    <div className="flex flex-col justify-between items-center w-full md:items-center">
                        <div className="grid grid-cols-5 md:grid-cols-4 gap-3 md:gap-4 mx-5">
                            <input
                                type="text"
                                value={anime}
                                autoFocus={true}
                                className="border-none text-black py-4 self-end outline-none col-span-4 md:col-span-3 bg-primary px-4 rounded-full font-rosarivo"
                                placeholder="Enter anime name..."
                                onChange={e => setAnime(e.target.value)}
                                required
                            />
                            <button
                                className="border-none outline-none focus:outline-none focus:border-none self-end col-span-2 text-sm md:text-lg md:col-span-1 px-5 md:px-12 py-3 rounded-full bg-blue-600 font-rosarivo ml-0 mt-4"
                                onClick={fetchAnimeResults}
                                disabled={btnStatus}
                            >
                                {btnTxt}
                            </button>
                        </div>
                    </div>
                </div>
                {recommendation &&
					recommendation.map((suggestion,index) => {
						return (
							<div
								className="flex flex-col item-center font-rosarivo my-12 w-4/5 h-4/5 md:flex-col md:w-4/6 md:h-full md:mb-12"
								key={index}
							>
								<div className="w-full mt-4 p-8 border border-secondary h-full text-lightGrey text-2xl">
                                    <div className="w-4/5 h-4/5 mx-auto overflow-hidden mb-10">
                                        <img
                                            src={suggestion.main_picture_large}
                                            alt= ""
                                        />
                                    </div>
									<h2 className="text-2xl font-bold my-4">
										{suggestion.title}
									</h2>
									<p className="text-base text-justify leading-8">
										{suggestion.synopsis}
									</p>
								</div>
							</div>
						);
					})}
            </div>
        </>
    )
}
