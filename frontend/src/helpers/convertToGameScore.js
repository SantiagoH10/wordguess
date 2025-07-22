// Convert -1 to 1 range into 0 to 100 scale

export const convertToGameScore = similarity => {
  return Math.max(0, Math.round((similarity + 1) * 50))
}
