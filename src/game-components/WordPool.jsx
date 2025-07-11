import { useGame } from '../logic/useGame'

import { useEffect, useRef } from "react";


const FireCard = ({ word }) => {
  return (
    <div className="relative overflow-hidden px-6 py-4 bg-gradient-to-t from-red-700 via-red-500 to-orange-400 text-white font-bold text-xl rounded-lg shadow-2xl transform transition-all duration-300 hover:scale-105 hover:shadow-red-500/50 group min-w-[120px]">
      {/* Fire glow effect */}
      <div className="absolute inset-0 bg-gradient-to-t from-red-600 via-orange-500 to-yellow-400 opacity-0 group-hover:opacity-70 transition-opacity duration-300 animate-pulse"></div>

      {/* Animated fire particles */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute bottom-0 left-1/4 w-2 h-2 bg-orange-400 rounded-full animate-bounce delay-0"></div>
        <div className="absolute bottom-0 left-1/2 w-1 h-1 bg-red-400 rounded-full animate-bounce delay-100"></div>
        <div className="absolute bottom-0 right-1/4 w-2 h-2 bg-yellow-400 rounded-full animate-bounce delay-200"></div>
        <div className="absolute bottom-1 left-1/3 w-1 h-1 bg-orange-300 rounded-full animate-bounce delay-300"></div>
        <div className="absolute bottom-1 right-1/3 w-1 h-1 bg-red-300 rounded-full animate-bounce delay-75"></div>
      </div>

      {/* Card text */}
      <p className="relative z-10 drop-shadow-lg text-center">
        {word}
      </p>

      {/* Inner glow */}
      <div className="absolute inset-0 rounded-lg bg-gradient-to-t from-transparent via-orange-300/20 to-yellow-200/30 group-hover:from-transparent group-hover:via-orange-200/30 group-hover:to-yellow-100/40 transition-all duration-300"></div>

      {/* Fire emoji indicator */}
      <div className="absolute -top-2 -right-2 text-2xl animate-pulse">
        🔥
      </div>
    </div>
  )
}

// Frozen Card Component
const FrozenCard = ({ word }) => {
  const cardRef = useRef(null);

  useEffect(() => {
    const createSnowflake = () => {
      if (!cardRef.current) return;

      const snowflake = document.createElement("div");
      snowflake.className = "absolute text-white select-none pointer-events-none";
      snowflake.innerText = "❄️";
      snowflake.style.left = Math.random() * cardRef.current.offsetWidth + "px";
      snowflake.style.top = "-20px";
      snowflake.style.fontSize = 8 + Math.random() * 12 + "px";
      snowflake.style.opacity = 0.6 + Math.random() * 0.4;
      snowflake.style.animationDuration = 3 + Math.random() * 4 + "s";
      snowflake.style.animation = `snowfall ${3 + Math.random() * 4}s linear infinite`;

      cardRef.current.appendChild(snowflake);

      setTimeout(() => {
        if (snowflake.parentNode) {
          snowflake.remove();
        }
      }, 8000);
    };

    const interval = setInterval(createSnowflake, 400);
    return () => {
      clearInterval(interval);
      // Clean up any remaining snowflakes
      if (cardRef.current) {
        const snowflakes = cardRef.current.querySelectorAll('.absolute');
        snowflakes.forEach(flake => flake.remove());
      }
    };
  }, []);

  return (
    <>
      <style jsx>{`
        @keyframes snowfall {
          0% {
            transform: translateY(-20px) rotate(0deg);
          }
          100% {
            transform: translateY(120px) rotate(360deg);
          }
        }
        @keyframes shimmer {
          0%, 100% {
            background-position: -200% center;
          }
          50% {
            background-position: 200% center;
          }
        }
      `}</style>

      <div
        ref={cardRef}
        className="relative overflow-hidden px-6 py-4 bg-gradient-to-t from-blue-800 via-blue-600 to-cyan-400 text-white font-bold text-xl rounded-lg shadow-2xl transform transition-all duration-300 hover:scale-105 hover:shadow-blue-500/50 group min-w-[120px] border-2 border-blue-300/30"
      >
        {/* Ice crystal overlay */}
        <div className="absolute inset-0 bg-gradient-to-br from-white/10 via-transparent to-blue-200/10 opacity-50"></div>

        {/* Frost effect */}
        <div className="absolute inset-0 bg-gradient-to-t from-transparent via-white/5 to-white/20 group-hover:from-transparent group-hover:via-white/10 group-hover:to-white/30 transition-all duration-300"></div>

        {/* Shimmer effect */}
        <div
          className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"
          style={{
            backgroundSize: '200% 100%',
            animation: 'shimmer 2s infinite'
          }}
        ></div>

        {/* Frozen particles (static ice crystals) */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-2 left-1/4 text-blue-200 opacity-60">✦</div>
          <div className="absolute top-4 right-1/4 text-cyan-200 opacity-40">❅</div>
          <div className="absolute bottom-3 left-1/3 text-blue-100 opacity-50">✧</div>
          <div className="absolute bottom-2 right-1/3 text-cyan-100 opacity-70">❄</div>
          <div className="absolute top-1/2 left-1/6 text-blue-200 opacity-30">❈</div>
        </div>

        {/* Card text */}
        <p className="relative z-10 drop-shadow-lg text-center text-blue-50">
          {word}
        </p>

        {/* Frozen emoji indicator */}
        <div className="absolute -top-2 -right-2 text-2xl">
          🧊
        </div>
      </div>
    </>
  )
}
// Warm Card Component
const WarmCard = ({ word }) => {
  const cardRef = useRef(null);

  useEffect(() => {
    const createSparkle = () => {
      if (!cardRef.current) return;

      const sparkle = document.createElement("div");
      sparkle.className = "absolute text-yellow-300 select-none pointer-events-none";
      sparkle.innerText = "✨";
      sparkle.style.left = Math.random() * cardRef.current.offsetWidth + "px";
      sparkle.style.top = Math.random() * cardRef.current.offsetHeight + "px";
      sparkle.style.fontSize = 8 + Math.random() * 8 + "px";
      sparkle.style.opacity = 0.7 + Math.random() * 0.3;
      sparkle.style.animationDuration = 2 + Math.random() * 3 + "s";
      sparkle.style.animation = `sparkleFloat ${2 + Math.random() * 3}s ease-in-out infinite`;

      cardRef.current.appendChild(sparkle);

      setTimeout(() => {
        if (sparkle.parentNode) {
          sparkle.remove();
        }
      }, 5000);
    };

    const interval = setInterval(createSparkle, 600);
    return () => {
      clearInterval(interval);
      // Clean up any remaining sparkles
      if (cardRef.current) {
        const sparkles = cardRef.current.querySelectorAll('.absolute');
        sparkles.forEach(sparkle => sparkle.remove());
      }
    };
  }, []);

  return (
    <>
      <style jsx>{`
        @keyframes sparkleFloat {
          0%, 100% {
            transform: translateY(0px) scale(1) rotate(0deg);
            opacity: 0.7;
          }
          50% {
            transform: translateY(-10px) scale(1.2) rotate(180deg);
            opacity: 1;
          }
        }
        @keyframes warmGlow {
          0%, 100% {
            box-shadow: 0 0 20px rgba(251, 146, 60, 0.3);
          }
          50% {
            box-shadow: 0 0 30px rgba(251, 146, 60, 0.6);
          }
        }
        @keyframes warmPulse {
          0%, 100% {
            background-position: 0% 50%;
          }
          50% {
            background-position: 100% 50%;
          }
        }
      `}</style>

      <div
        ref={cardRef}
        className="relative overflow-hidden px-6 py-4 bg-gradient-to-br from-orange-500 via-amber-400 to-yellow-400 text-white font-bold text-xl rounded-lg shadow-2xl transform transition-all duration-300 hover:scale-105 group min-w-[120px] border-2 border-orange-300/40"
        style={{
          animation: 'warmGlow 3s ease-in-out infinite'
        }}
      >
        {/* Warm gradient overlay */}
        <div className="absolute inset-0 bg-gradient-to-r from-orange-400/20 via-yellow-300/30 to-orange-400/20 opacity-60 group-hover:opacity-80 transition-opacity duration-300"
             style={{
               backgroundSize: '200% 200%',
               animation: 'warmPulse 4s ease-in-out infinite'
             }}></div>

        {/* Heat shimmer effect */}
        <div className="absolute inset-0 bg-gradient-to-t from-transparent via-yellow-200/10 to-orange-200/20 group-hover:from-transparent group-hover:via-yellow-200/20 group-hover:to-orange-200/30 transition-all duration-300"></div>

        {/* Warm particles (static golden elements) */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-2 left-1/4 text-yellow-200 opacity-70 animate-pulse">●</div>
          <div className="absolute top-4 right-1/4 text-orange-200 opacity-60 animate-pulse delay-100">○</div>
          <div className="absolute bottom-3 left-1/3 text-yellow-300 opacity-50 animate-pulse delay-200">●</div>
          <div className="absolute bottom-2 right-1/3 text-orange-300 opacity-80 animate-pulse delay-300">○</div>
          <div className="absolute top-1/2 left-1/6 text-amber-200 opacity-40 animate-pulse delay-150">●</div>
          <div className="absolute top-1/3 right-1/6 text-yellow-400 opacity-60 animate-pulse delay-250">○</div>
        </div>

        {/* Gentle heat waves */}
        <div className="absolute bottom-0 left-0 right-0 h-8 bg-gradient-to-t from-orange-400/30 to-transparent opacity-50 group-hover:opacity-70 transition-opacity duration-300"></div>

        {/* Card text */}
        <p className="relative z-10 drop-shadow-lg text-center text-orange-50">
          {word}
        </p>

        {/* Warm emoji indicator */}
        <div className="absolute -top-2 -right-2 text-2xl animate-pulse">
          ☀️
        </div>
      </div>
    </>
  )
}

/*
const WordCard = ({ children }) => {
 const getCardStyle = (score) => {
   if (score <= 50) {
     // Frozen style
     return "rounded-lg bg-gradient-to-br from-blue-400 to-blue-600 border-2 border-blue-300/50 shadow-lg shadow-blue-500/25"
   } else if (score <= 80) {
     // Warm style
     return "rounded-lg bg-gradient-to-br from-orange-400 to-orange-600 border-2 border-orange-300/50 shadow-lg shadow-orange-500/25"
   } else {
     // On fire style
     return "rounded-lg bg-gradient-to-br from-red-500 to-red-700 border-2 border-red-300/50 shadow-lg shadow-red-500/25 animate-pulse"
   }
 }


 const getTextStyle = (score) => {
   if (score <= 50) {
     return "text-blue-100 font-medium"
   } else if (score <= 80) {
     return "text-orange-100 font-semibold"
   } else {
     return "text-red-100 font-bold"
   }
 }

 return (
   <div className={getCardStyle(children.score)}>
     <p className={getTextStyle(children.score)}>{children.word}</p>
   </div>
 )
}
*/

const WordCard = ({ word, score }) => {
  if (score <= 50) {
    return <FrozenCard word={word}/>
  } else if (score <= 80) {
    return <WarmCard word={word}/>
  } else {
    return <FireCard word={word}/>
  }
}




export function WordPool() {
 const { wordPool } = useGame()

 return (
   <div className="backdrop-blur-md bg-white/10 border border-white/20 rounded-2xl p-6 shadow-xl">
     {/* Inner glow effect */}
     <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-white/5 to-transparent pointer-events-none"></div>

     {/* Content container */}
     <div className="relative z-10 flex flex-wrap gap-4 justify-center">
       {wordPool.map(i => (
         <WordCard key={i.id} word={i.word} score={i.score}/>
       ))}
     </div>

     {/* Optional header */}
     <div className="mb-4 text-center">
       <h3 className="text-white/80 font-semibold text-lg">Word Pool</h3>
       <p className="text-white/60 text-sm">{wordPool.length} words</p>
     </div>
   </div>
 )
}
