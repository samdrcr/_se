interface Room {
  id: string;
  occupants: number;
  squareMeters: number;
}

// Test case initialized for a large multi-floor house
export const houseConfig: Room[] = [
  { id: "Lantai_1_Room", occupants: 2, squareMeters: 25 },
  { id: "Lantai_2_RoomA", occupants: 1, squareMeters: 15 },
  { id: "Lantai_2_RoomB", occupants: 1, squareMeters: 18 },
  // Add remaining rooms up to 8-10 occupants...
];

export function calculateRentSplit(totalRent: number, rooms: Room[]) {
  const totalOccupants = rooms.reduce((sum, room) => sum + room.occupants, 0);
  const totalArea = rooms.reduce((sum, room) => sum + room.squareMeters, 0);

  // 50% of rent based on head count (common areas), 50% based on room size
  return rooms.map(room => {
    const headCountShare = (totalRent * 0.5) * (room.occupants / totalOccupants);
    const spaceShare = (totalRent * 0.5) * (room.squareMeters / totalArea);
    
    return {
      roomId: room.id,
      totalRoomRent: Math.round(headCountShare + spaceShare),
      rentPerOccupant: Math.round((headCountShare + spaceShare) / room.occupants)
    };
  });
}
