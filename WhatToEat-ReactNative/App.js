import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, TouchableOpacity } from 'react-native';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import RouletteWheel from './src/components/RouletteWheel';

export default function App() {
  const handleSpinEnd = (selectedItem) => {
    console.log('Selected:', selectedItem);
  };

  const handleRandomSpin = () => {
    // 랜덤 스핀 로직은 RouletteWheel 내부에서 처리
  };

  return (
    <GestureHandlerRootView style={styles.container}>
      <View style={styles.background}>
        {/* 헤더 */}
        <View style={styles.header}>
          <Text style={styles.title}>오늘 뭐먹지?</Text>
          <Text style={styles.subtitle}>프리미엄 룰렛으로 선택하세요</Text>
        </View>

        {/* 룰렛 */}
        <RouletteWheel onSpinEnd={handleSpinEnd} />

        {/* 스핀 버튼 */}
        <View style={styles.buttonContainer}>
          <TouchableOpacity style={styles.spinButton} onPress={handleRandomSpin}>
            <Text style={styles.spinButtonText}>🎯 랜덤 스핀</Text>
          </TouchableOpacity>
        </View>

        <StatusBar style="light" />
      </View>
    </GestureHandlerRootView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  background: {
    flex: 1,
    backgroundColor: '#667eea',
    backgroundImage: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  },
  header: {
    paddingTop: 60,
    paddingBottom: 20,
    alignItems: 'center',
    zIndex: 5,
  },
  title: {
    color: '#ffffff',
    fontSize: 28,
    fontWeight: '800',
    textShadowColor: 'rgba(0,0,0,0.3)',
    textShadowOffset: { width: 0, height: 2 },
    textShadowRadius: 4,
    marginBottom: 8,
  },
  subtitle: {
    color: 'rgba(255,255,255,0.9)',
    fontSize: 16,
    fontWeight: '400',
  },
  buttonContainer: {
    position: 'absolute',
    bottom: 100,
    left: 0,
    right: 0,
    alignItems: 'center',
    zIndex: 5,
  },
  spinButton: {
    backgroundColor: '#ffffff',
    paddingHorizontal: 32,
    paddingVertical: 16,
    borderRadius: 30,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  spinButtonText: {
    color: '#667eea',
    fontSize: 18,
    fontWeight: 'bold',
  },
});
