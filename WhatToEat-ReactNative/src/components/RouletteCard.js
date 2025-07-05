import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { CATEGORY_COLORS } from '../data/MenuData';

const RouletteCard = ({ item, index, totalCards, cardSize }) => {
  const angle = (index * 360) / totalCards;
  const rotation = `${angle}deg`;

  const getCardStyle = () => {
    const categoryColor = CATEGORY_COLORS[item.id] || CATEGORY_COLORS.chicken;
    
    let backgroundColor = categoryColor.bg;
    if (item.type === 'coupang') {
      backgroundColor = '#ffd700';
    } else if (item.type === 'ranking') {
      backgroundColor = '#ff7043';
    }

    return {
      ...styles.card,
      width: cardSize.width,
      height: cardSize.height,
      backgroundColor,
      transform: [
        { rotate: rotation },
        { translateY: -cardSize.radius }
      ]
    };
  };

  const getHeaderStyle = () => {
    if (item.type === 'coupang') {
      return { ...styles.cardHeader, backgroundColor: '#ffb300' };
    } else if (item.type === 'ranking') {
      return { ...styles.cardHeader, backgroundColor: '#ff5722' };
    }
    
    const categoryColor = CATEGORY_COLORS[item.id] || CATEGORY_COLORS.chicken;
    return { ...styles.cardHeader, backgroundColor: categoryColor.theme };
  };

  return (
    <View style={getCardStyle()}>
      <View style={getHeaderStyle()}>
        <Text style={styles.cardTitle}>{item.title}</Text>
        {(item.type === 'coupang' || item.type === 'ranking') && (
          <Text style={styles.adBadge}>{item.rank}</Text>
        )}
      </View>
      
      <View style={styles.cardContent}>
        {item.items.slice(0, 3).map((menuItem, idx) => (
          <View key={idx} style={styles.menuItem}>
            <Text style={styles.menuIcon}>{menuItem.icon}</Text>
            <View style={styles.menuInfo}>
              <Text style={styles.menuName}>{menuItem.name}</Text>
              <Text style={styles.menuTag}>{menuItem.tag}</Text>
            </View>
            {menuItem.rank && (
              <Text style={styles.menuRank}>{menuItem.rank}</Text>
            )}
          </View>
        ))}
        
        {item.items.length > 3 && (
          <Text style={styles.moreItems}>+{item.items.length - 3}개 더</Text>
        )}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    position: 'absolute',
    borderRadius: 8,
    borderWidth: 2,
    borderColor: '#ffffff',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5,
    overflow: 'hidden'
  },
  cardHeader: {
    padding: 8,
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'space-between'
  },
  cardTitle: {
    color: '#ffffff',
    fontSize: 12,
    fontWeight: 'bold',
    flex: 1
  },
  adBadge: {
    color: '#ffffff',
    fontSize: 10,
    fontWeight: 'bold',
    backgroundColor: 'rgba(0,0,0,0.2)',
    paddingHorizontal: 4,
    paddingVertical: 2,
    borderRadius: 4
  },
  cardContent: {
    padding: 8,
    flex: 1
  },
  menuItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 2,
    marginBottom: 4
  },
  menuIcon: {
    fontSize: 14,
    marginRight: 6
  },
  menuInfo: {
    flex: 1
  },
  menuName: {
    fontSize: 10,
    fontWeight: '600',
    color: '#333'
  },
  menuTag: {
    fontSize: 8,
    color: '#666',
    marginTop: 1
  },
  menuRank: {
    fontSize: 9,
    fontWeight: 'bold',
    color: '#ff6b35',
    marginLeft: 4
  },
  moreItems: {
    fontSize: 8,
    color: '#888',
    textAlign: 'center',
    marginTop: 4,
    fontStyle: 'italic'
  }
});

export default RouletteCard;