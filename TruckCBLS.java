package class124193.pqd;

import java.io.File;
import java.util.ArrayList;
import java.util.Random;
import java.util.Scanner;

import localsearch.constraints.basic.AND;
import localsearch.constraints.basic.Implicate;
import localsearch.constraints.basic.IsEqual;
import localsearch.constraints.basic.LessOrEqual;
import localsearch.constraints.basic.OR;
import localsearch.functions.basic.FuncMinus;
import localsearch.functions.basic.FuncMult;
import localsearch.functions.basic.FuncPlus;
import localsearch.functions.conditionalsum.ConditionalSum;
import localsearch.model.ConstraintSystem;
import localsearch.model.IConstraint;
import localsearch.model.IFunction;
import localsearch.model.LocalSearchManager;
import localsearch.model.VarIntLS;

public class TruckCBLS {
	int N;
	int K;
	int[] w;
	int[] l;
	int[] W;
	int[] L;
	int[] c;
	
	int maxW = 0;
	int maxL = 0;
	int sumC = 0;
	//modeling
	LocalSearchManager mgr;
	ConstraintSystem CS;
	VarIntLS[] x1;
	VarIntLS[] y1;
	VarIntLS[] p;
	VarIntLS[] o;
	VarIntLS[] u;
	
	// o=1 <=> x2[i]=x[1]+w[i]
	// o=0 <=> x2[i]=x[1]+l[i]
	// x2[i] = x1[i] + o[i]*w[i] - (o[i]-1)*l[i]
	// y2[i] = y1[i] + o[i]*l[i] - (o[i]-1)*w[i]
	IFunction[] x2;
	IFunction[] y2;
	// of1 = o[i]-1
	// xf1 = o[i]*w[i]
	// xf2 = (o[i]-1)*l[i]
	//because The constructor FuncMinus(int, VarIntLS) is undefined
	// xf3 = o[i]*w[i] - (o[i]-1)*l[i]
	IFunction[] of1;
	IFunction[] xf1;
	IFunction[] xf2;
	IFunction[] xf3;
	IFunction[] yf1;
	IFunction[] yf2;
	IFunction[] yf3;	
	
	IFunction obj;
	public void stateModel() {
		mgr = new LocalSearchManager();
		CS = new ConstraintSystem(mgr);
		x1 = new VarIntLS[N];
		y1 = new VarIntLS[N];
		p = new VarIntLS[N];
		o = new VarIntLS[N];
		u = new VarIntLS[N];
		
		for(int i = 0; i < N; i++) {
			x1[i] = new VarIntLS(mgr, 0, maxW);
			y1[i] = new VarIntLS(mgr, 0, maxL);
			p[i] = new VarIntLS(mgr, 0, K-1);
			o[i] = new VarIntLS(mgr, 0, 1);
			u[i] = new VarIntLS(mgr, 0, 1);
		}
		
		x2 = new IFunction[N];
		y2 = new IFunction[N];
		of1 = new IFunction[N];
		xf1 = new IFunction[N];
		xf2 = new IFunction[N];
		xf3 = new IFunction[N];
		yf1 = new IFunction[N];
		yf2 = new IFunction[N];
		yf3 = new IFunction[N];
		
		for(int i = 0; i < N; i++) {
			of1[i] = new FuncMinus(o[i], 1);
			xf1[i] = new FuncMult(o[i], w[i]);
			xf2[i] = new FuncMult(of1[i], l[i]);
			xf3[i] = new FuncMinus(xf1[i], xf2[i]);
			x2[i] = new FuncPlus(xf3[i], x1[i]);
			
			yf1[i] = new FuncMult(o[i], l[i]);
			yf2[i] = new FuncMult(of1[i], w[i]);
			yf3[i] = new FuncMinus(yf1[i], yf2[i]);
			y2[i] = new FuncPlus(yf3[i], y1[i]);
			
			for(int j = 0; j < K; j++) {
				IConstraint[] cSize = new IConstraint[2];
				cSize[0] = new LessOrEqual(x2[i], W[j]);
				cSize[1] = new LessOrEqual(y2[i], L[j]);
				IsEqual piEqualJ = new IsEqual(p[i], j);
				Implicate implicateSize = new Implicate(piEqualJ, new AND(cSize));
				CS.post(implicateSize);
				// p[i] = j => u[j] = 1
				Implicate implicateUseTruck = new Implicate(piEqualJ, new IsEqual(u[j], 1));
				CS.post(implicateUseTruck);
			}
		}
		for(int i = 0; i < N; i++) {
			for(int i2 = i+1; i2 < N; i2++) {
				IConstraint[] cOr = new IConstraint[4];
				cOr[0] = new LessOrEqual(x2[i], x1[i2]);
				cOr[1] = new LessOrEqual(x2[i2], x1[i]);
				cOr[2] = new LessOrEqual(y2[i], y1[i2]);
				cOr[3] = new LessOrEqual(y2[i2], y1[i]);
				Implicate implicate = new Implicate(new IsEqual(p[i], p[i2]), new OR(cOr));
				CS.post(implicate);
			}
		}
		// u[j] = 1 => exist p[i] = j
		for(int j = 0; j < K; j++) {
			IConstraint[] cOr = new IConstraint[N];
			for(int i = 0; i < N; i++) {
				cOr[i] = new IsEqual(p[i], j);
			}
			Implicate implicateUseTruck = new Implicate(new IsEqual(u[j], 1), new OR(cOr));
			CS.post(implicateUseTruck);
		}
		
		obj = new ConditionalSum(u, c, 1);
		mgr.close();
	}
	class Move{
		static final int MOVE_O = 0;
		static final int MOVE_X1 = 1;
		static final int MOVE_Y1 = 2;
		static final int MOVE_P = 3;
		static final int MOVE_U = 4;
		
		int type;
		int i;
		int v;
		public Move(int type, int i, int v){
			this.type = type; this.i = i; this.v = v;
		}
	}
	public void search(int maxIters, int maxTime) {
		int it = 0;
		Random R = new Random();
		System.out.println("Init, CS = " + CS.violations() + " obj = " + obj.getValue());
		
		ArrayList<Move> cand = new ArrayList<Move>();
		double t0 = System.currentTimeMillis();
		while(it < maxIters){
			int minDeltaC = Integer.MAX_VALUE;
			int minDeltaF = Integer.MAX_VALUE;
			for(int i = 0; i < N; i++){
				for(int v = o[i].getMinValue(); v <= o[i].getMaxValue(); v++){
					double t= System.currentTimeMillis() - t0;
					if(t > maxTime){
						System.out.println("Time limit exceeded!");
						break;
					}
					int deltaC = CS.getAssignDelta(o[i], v);
					int deltaF = obj.getAssignDelta(o[i], v);
					if(deltaC < minDeltaC || deltaC == minDeltaC && deltaF < minDeltaF){
						cand.clear();
						cand.add(new Move(Move.MOVE_O, i, v));
						minDeltaC = deltaC; minDeltaF = deltaF;
					}else if(deltaC == minDeltaC && deltaF == minDeltaF){
						cand.add(new Move(Move.MOVE_O, i, v));
					}
				}
			}
			for(int i = 0; i < N; i++){
				for(int v = x1[i].getMinValue(); v <= x1[i].getMaxValue(); v++){
					double t= System.currentTimeMillis() - t0;
					if(t > maxTime){
						System.out.println("Time limit exceeded!");
						break;
					}
					
					int deltaC = CS.getAssignDelta(x1[i], v);
					int deltaF = obj.getAssignDelta(x1[i], v);
					if(deltaC < minDeltaC || deltaC == minDeltaC && deltaF < minDeltaF){
						cand.clear();
						cand.add(new Move(Move.MOVE_X1, i, v));
						minDeltaC = deltaC; minDeltaF = deltaF;
					}else if(deltaC == minDeltaC && deltaF == minDeltaF){
						cand.add(new Move(Move.MOVE_X1, i, v));
					}
				}
			}
			for(int i = 0; i < N; i++){
				for(int v = y1[i].getMinValue(); v <= y1[i].getMaxValue(); v++){
					double t= System.currentTimeMillis() - t0;
					if(t > maxTime){
						System.out.println("Time limit exceeded!");
						break;
					}
					
					int deltaC = CS.getAssignDelta(y1[i], v);
					int deltaF = obj.getAssignDelta(y1[i], v);
					if(deltaC < minDeltaC || deltaC == minDeltaC && deltaF < minDeltaF){
						cand.clear();
						cand.add(new Move(Move.MOVE_Y1, i, v));
						minDeltaC = deltaC; minDeltaF = deltaF;
					}else if(deltaC == minDeltaC && deltaF == minDeltaF){
						cand.add(new Move(Move.MOVE_Y1, i, v));
					}
				}
			}
			for(int i = 0; i < N; i++){
				for(int v = p[i].getMinValue(); v <= p[i].getMaxValue(); v++){
					double t= System.currentTimeMillis() - t0;
					if(t > maxTime){
						System.out.println("Time limit exceeded!");
						break;
					}
					
					int deltaC = CS.getAssignDelta(p[i], v);
					int deltaF = obj.getAssignDelta(p[i], v);
					if(deltaC < minDeltaC || deltaC == minDeltaC && deltaF < minDeltaF){
						cand.clear();
						cand.add(new Move(Move.MOVE_P, i, v));
						minDeltaC = deltaC; minDeltaF = deltaF;
					}else if(deltaC == minDeltaC && deltaF == minDeltaF){
						cand.add(new Move(Move.MOVE_P, i, v));
					}
				}
			}
			for(int i = 0; i < N; i++){
				for(int v = u[i].getMinValue(); v <= u[i].getMaxValue(); v++){
					double t= System.currentTimeMillis() - t0;
					if(t > maxTime){
						System.out.println("Time limit exceeded!");
						break;
					}
					
					int deltaC = CS.getAssignDelta(u[i], v);
					int deltaF = obj.getAssignDelta(u[i], v);
					if(deltaC < minDeltaC || deltaC == minDeltaC && deltaF < minDeltaF){
						cand.clear();
						cand.add(new Move(Move.MOVE_U, i, v));
						minDeltaC = deltaC; minDeltaF = deltaF;
					}else if(deltaC == minDeltaC && deltaF == minDeltaF){
						cand.add(new Move(Move.MOVE_U, i, v));
					}
				}
			}
			
			Move m = cand.get(R.nextInt(cand.size()));
			if(m.type == Move.MOVE_O) {
				o[m.i].setValuePropagate(m.v);
			} else if(m.type == Move.MOVE_X1) {
				x1[m.i].setValuePropagate(m.v);
			} else if(m.type == Move.MOVE_Y1) {
				y1[m.i].setValuePropagate(m.v);
			} else if(m.type == Move.MOVE_P){
				p[m.i].setValuePropagate(m.v);
			} else {
				u[m.i].setValuePropagate(m.v);
			}
			it++;
			double t= Math.round((System.currentTimeMillis() - t0)/6)/10000.0;
			System.out.println("Step it = " + it + " time = " + t + " CS = " + CS.violations() + 
					" obj = " + obj.getValue());
		}
	}
	public void readData(String filename) {
		try {
			Scanner in = new Scanner(new File(filename));
			N = in.nextInt();
			K = in.nextInt();
			w = new int[N];
			l = new int[N];
			for(int i = 0; i < N; i++) {
				w[i] = in.nextInt();
				l[i] = in.nextInt();
			}
			W = new int[K];
			L = new int[K];
			c = new int[K];
			for(int j = 0; j < K; j++) {
				W[j] = in.nextInt();
				L[j] = in.nextInt();
				c[j] = in.nextInt();
				sumC += c[j];
				if(W[j] > maxW) {
					maxW = W[j];
				}
				if(L[j] > maxL) {
					maxL = L[j];
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	public void printResult() {
		for(int i = 0; i < N; i++) {
			System.out.printf("package %d at truck %d, orientation %d, bottom-left: (%d, %d), top-right: (%d, %d)\n",
					i, p[i].getValue(), o[i].getValue(), x1[i].getValue(), y1[i].getValue(), x2[i].getValue(), y2[i].getValue());
		}
	}
	public void printData() {
		System.out.println(N + " " + K);
		int S = 0;
		for(int i = 0; i < N; i++) {
			System.out.println("package "+i+": "+w[i]+" "+l[i]);
			S += w[i] * l[i];
		}
		System.out.println("Total area: " + S);
		System.out.println("=========");
		for(int j = 0; j < K; j++) {
			System.out.println("truck "+j+": "+W[j]+" "+L[j]+" "+c[j]);
		}
		System.out.println("=========");
	}
	public static void main(String[] args) {
		TruckCBLS app = new TruckCBLS();
		app.readData("data/Truck/test-data-1.txt");
		app.printData();
		app.stateModel();
		app.search(1000000, 1800000);
		app.printData();
		app.printResult();
	}

}
