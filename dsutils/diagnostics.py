# -*- coding: utf-8 -*-
"""Diagnostics.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19bf30ZZofd3zsCNPyRQEg4y3ZhInwWy-
"""

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import average_precision_score
from sklearn.metrics import precision_recall_curve
from sklearn.utils.multiclass import unique_labels
import seaborn as sn
import numpy as np
from matplotlib.pyplot import cm
import sklearn
import scikitplot as skplt
import argparse

class Diagnostics(object):
    """
    Class that creates plots for regression or classification problems in machine learning problems
    
    Attributes:
        actual - list or array, the true labels inputted into model
        predicted - list or array, the predicted labels outputted by your model
        acc - list or array, in format: [acc_train_per_epoch, acc_validation_per_epoch]
        loss - list or array, in format: [loss_train_per_epoch, loss_validation_per_epoch]
        auc - list or array, in format: [auc_train_per_epoch, auc_validation_per_epoch]
        feature_list - list, features used to train model
        cross_val 
        data_batch - array, batch of image pixels 
        labels_batch - array, labels matching data_batch images
    """
    
    # Plot axes formatting
    plt.rcParams['axes.linewidth']=3
    plt.rcParams['xtick.major.width'] = 2
    plt.rcParams['ytick.major.width'] = 2
    plt.rcParams['xtick.minor.width'] = 2
    plt.rcParams['ytick.minor.width'] = 2
    plt.rc('xtick.major', size=8, pad=8)
    plt.rc('xtick.minor', size=6, pad=5)
    plt.rc('ytick.major', size=8, pad=8)
    plt.rc('ytick.minor', size=6, pad=5)
    
    def __init__(self, actual, predicted, acc=0, loss=0, auc=0, feature_list=0, cross_val=0, data_batch=0, labels_batch=0):
        # Mandatory lists for diagnostics
        self.actual=actual
        self.predicted=predicted 

        # User-added lists for diagnostics
        self.acc=acc; self.loss=loss; self.auc = auc
        self.feature_lists=feature_list
        self.cross_val=cross_val
        self.data = data_batch
        self.labels_batch = labels_batch
    
    def convert_to_index(self, array_categorical):
        array_index = [np.argmax(array_temp) for array_temp in array_categorical]
        return array_index

      
    # Plots confusion matrix. If norm is set, values are between 0-1. Shows figure if show is set
    def plot_cm(self, figsize = (6, 4), norm=True, show=True):
        """
        Creates a confusion matrix for the predicted and actual labels for your model

        Input:
           - figsize: tuple, the figure size of the desired plot
           - norm: boolean, whether or not you want your confusion matrix normalized (between 0-1)
           - show: boolean, whether you want to plt.show() your figure or just save it to your computer 
        """
        #if self.actual == None or self.predicted == None:
            #raise NameError("Missing either actual predicted labels")
        
        #if (len(self.actual) != len(self.predicted)):
            #raise NameError("Predicted and actual labels must be same shape")
            
        #converting raw labels into a 1D list
        actual_lbl = self.convert_to_index(self.actual)
        pred_lbl = self.convert_to_index(self.predicted)
            
        cm=confusion_matrix(actual_lbl, pred_lbl)
        plt.figure(figsize=figsize)
        labels = np.unique(pred_lbl).tolist()
        np.set_printoptions(precision=2)

        if (norm):
            heatmap_value = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
            file_name = "Confusion_Matrix_Norm.jpeg"
            plt.title("Normalized Confusion Matrix", fontsize=18)

        else:
            heatmap_value = cm.astype('float')
            file_name = "Confusion_Matrix.jpeg"
            plt.title("Confusion Matrix", fontsize=14)

        sn.heatmap(heatmap_value, annot=True, xticklabels=labels, yticklabels=labels, 
                   cmap="Blues", annot_kws={"size": 10}, fmt='.2f')

        plt.yticks(fontsize=14)
        plt.xticks(fontsize=14)
        plt.ylabel("True Label", fontsize=14)
        plt.xlabel("Predicted Label", fontsize=14)

        plt.savefig(file_name)
        if (show): plt.show()
        plt.close()
    
    
    def plot_metrics_per_epoch(self, figsize = (15, 4), name_plot=[0,1,2], figname="metrics.png", show=True):
        """
        Plots accuracy, loss, and auc curves per epoch

        Input: 
        - figsize: tuple, the size of the metric curve
        - name_plot: list, whether you want '0' (loss), '1' (accuracy), and/or '2' (auc) plots, default plots all three
        - show: boolean, whether you want to plt.show() your figure or just save it to your computer 
        """
        num_graphs = len(name_plot)
        fig, axes = plt.subplots(nrows=1, ncols=num_graphs, figsize=figsize)
        
        for i, ele in enumerate(name_plot):
            if (ele == 0):
                metric_epoch_train = self.loss[0]
                metric_epoch_valid = self.loss[1]
                name_plot = "Loss"
            elif (ele == 1):
                metric_epoch_train = self.acc[0]
                metric_epoch_valid = self.acc[1]
                name_plot = "Accuracy"
            elif (ele == 2):
                metric_epoch_train = self.auc[0]
                metric_epoch_valid = self.auc[1]
                name_plot = "AUC"
            else:
                raise NameError("Improper value inputted, ignoring value")
                break

            axes[i].plot(metric_epoch_train, '-', color='seagreen', label='Training')
            axes[i].plot(metric_epoch_valid, '--', color='blue', label='Validation')
            axes[i].set_title("Epoch vs. " + name_plot, fontsize=20)
            
            axes[i].set_xlabel("Epoch", fontsize=16)
            axes[i].set_ylabel(name_plot, fontsize=16)
            axes[i].tick_params(labelsize=16)
            axes[i].legend(loc='best')
            
            extent = axes[i].get_window_extent().transformed(fig.dpi_scale_trans.inverted())
            fig.savefig("Epoch vs " + name_plot, bbox_inches=extent.expanded(1.1, 1.2))

        #plt.subplots_adjust(wspace=0.35, hspace=0.35)
        #fig.savefig(figname, bbox_inches='tight', transparent=True)
        if (show): fig.show()
        fig.close()
    
    # need to fix this function
    def plot_cross_validation(self, figsize = (6, 4), show=True):
        file_name = "K_fold_Cross_Validation.jpeg"
        plt.figure(figsize=figsize)
        plt.tile("K-fold Cross Validation", fontsize=14)
        plt.yticks(fontsize=14)
        plt.xticks(fontsize=14)
        plt.ylabel("Folds", fontsize=14)
        plt.xlabel("Accuracy", fontsize=14)
        plt.plot(self.loss)
        plt.savefig(file_name)
        if (show): plt.show()
        plt.close()
    
    
    def ROC_plot(self, figsize = (6, 4), show=True):
        """
        Plots the ROC curve between the predicted and actual labels
        Note: "actual" labels must be a 1D array

        Input:
          - figsize: tuple, the desired size of the image
          - show: boolean, whether you want to plt.show() your figure or just save it to your computer 
        """
        actual_lbl = self.convert_to_index(self.actual)
        #actual_lbl = [np.argmax(array_temp) for array_temp in self.actual]
        skplt.metrics.plot_roc(actual_lbl, self.predicted, figsize=figsize)
        if (show): plt.show()
        plt.close()
                                          
    
    def residual_dist_by_feature(self, figsize = (6,8), target='Target', hex_bin=False, show=True):
        file_name = '{}_errors_by_feature.pdf'.format(target)
        #Calculate residuals as fractional error.
        error=2*(self.predicted-self.actual)/(abs(self.actual)+abs(self.predicted))
        num_features=len(self.feature_list.columns); figure_width, figure_height = figsize
        fig=plt.figure(figsize=(figure_width, figure_height*num_features))
        for i in range(0, num_features):
            ax = fig.add_subplot(num_features, 1, i+1)
            #Plot the errors vs. feature.
            if hex_bin==True:
                ax.hexbin(feature_list[feature_list.columns[i]],error, bins='log')
            else:
                ax.plot(feature_list[feature_list.columns[i]],error, '.', alpha=0.2)
            ax.set_xlabel(feature_list.columns[i], fontsize=14)
            ax.set_ylabel('Fractional Error', fontsize=14)
            plt.rc('xtick',labelsize=14)
            plt.rc('ytick',labelsize=14)
            ax.set_title('Fractional Error as a function of {}'.format(feature_list.columns[i]), fontsize=14)
            extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
            plt.savefig(file_name, bbox_inches=extent)
        if (show): fig.show()
        fig.close()
    
    
    def one_to_one_plot(self, target_name='Target', axis_scale='linear', show=True):
        file_name = '{}_One_to_One.pdf'.format(target_name)
        plt.plot(self.actual, self.predicted, '.')
        plt.yticks(fontsize=14)
        plt.xticks(fontsize=14)
        plt.xlabel('True {}'.format(target_name), fontsize=14)
        plt.ylabel('Predicted {}'.format(target_name), fontsize=14)
        plt.title('One to one plot showing predicted vs. true {}'.format(target_name), fontsize=14)
        plt.xscale(axis_scale)
        plt.yscale(axis_scale)
        line_x, line_y = np.arange(min(self.actual),1.1*max(self.actual),(max(self.actual)-min(self.actual))/10), np.arange(min(self.actual),1.1*max(self.actual),(max(self.actual)-min(self.actual))/10)
        plt.plot(line_x,line_y,'r--')
        plt.savefig(file_name)
        if (show): plt.show()
        plt.close()
    
    
    def target_distributions(self, figsize=(6, 4), target='Target', x_scale='linear', y_scale='linear', show=True):
        file_name = '{}_distributions.pdf'.format(target)
        # Assign colors for each group and the names
        colors = ['#E69F00', '#56B4E9']
        names = ['True {}'.format(target), 'Predicted {}'.format(target)]
        
        actual_lbls = self.convert_to_index(self.actual)
        pred_lbls = self.convert_to_index(self.predicted)
        
        plt.figure(figsize=figsize)
        plt.hist([actual_lbls, pred_lbls], color=colors, label=names)
        plt.yscale(y_scale)
        plt.xscale(x_scale)
        plt.yticks(fontsize=14)
        plt.xticks(fontsize=14)
        # Plot formatting
        plt.legend()
        plt.xlabel(target, fontsize=14)
        plt.title('{} distributions for True and Predicted'.format(target), fontsize=14)
        plt.savefig(file_name)
        if (show): plt.show()
        plt.close()

    def plot_sample_img(self, figsize=(10, 10), filename="Image_Sample.png", show=True):
        """
        Plots data where each row of the plot consists of the same image in different channels (bands)

        Input:
          - data: array, an array of shape [batch_size, channels, height, width] OR [batch_size, height, width, channels]
          - labels: array, a 1D array of labels that match to the corresponding data
          - figsize: tuple, the figure size of the main plot
          - filename: string, saved filename
          - show: boolean, whether you want to plt.show() your figure or just save it to your computer  
        """

        plt.figure(figsize=figsize)
        
        num_imgs = len(self.data)
        counter = 1
        labels = self.convert_to_index(self.labels_batch)

        # if the image data is in the format [batch_size, channels, height, width]
        if (self.data.shape)[1] < (self.data.shape)[3]:
            num_bands = (self.data.shape)[1]
        # if the image data is in the format [batch_size, height, width, channels]
        else:
            num_bands = (self.data.shape)[3]
            
        for i in range(len(self.data)):
            for j in range(num_bands):
                #format plot horizontally
                if num_bands == 1:
                    plt.subplot(num_bands, num_imgs, counter)
                #format plot vertically
                else:
                    plt.subplot(num_imgs, num_bands, counter)                
                # if data format in shape [batch_size, channels, height, width]
                if (self.data.shape)[1] < (self.data.shape)[3]:
                    plt.imshow(self.data[i][j], cmap='gray')
                # if data format in shape [batch_size, height, width, channels]
                else:
                    plt.imshow(self.data[i, :, :, j], cmap='gray')
                plt.title("Label: "+ str(labels[i]), fontsize=14)
                counter += 1
        
        plt.subplots_adjust(wspace=.35, hspace=.35)
        plt.savefig(filename)
        if (show): plt.show()

                                          
    def output_average_precision(self):
        average_precision = average_precision_score(self.actual, self.predicted)
        print('Average precision-recall score: {0:0.2f}'.format(average_precision))
                                          
   
    def precision_recall_plot(self, show=True):
        plt.figure()
        actual_lbl = self.convert_to_index(self.actual)
        pred_lbl = self.convert_to_index(self.predicted)
        
        preicision, recall = precision_recall_curve(actual_lbl, pred_lbl)
        tep_kwargs = ({'step': 'post'}
               if 'step' in signature(plt.fill_between).parameters
               else {})
        plt.step(recall, precision, color='b', alpha=0.2,
         where='post')
        plt.fill_between(recall, precision, alpha=0.2, color='b', **step_kwargs)

        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        plt.title('2-class Precision-Recall curve: AP={0:0.2f}'.format(
          average_precision))
        if (show): plt.show(); plt.close()
                                          
    def run_diagnostics(self):
        """
        Runs through all of the available plotting methods and displays results
        """
        self.plot_sample_img()
        self.plot_metrics_per_epoch()
        self.plot_cm()
        self.ROC_plot()
        self.target_distributions()
        self.output_average_precision()
        
        